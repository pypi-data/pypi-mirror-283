from mypy.nodes import GDEF, AssignmentStmt, CastExpr, NameExpr, SymbolTableNode
from mypy.plugin import AnalyzeTypeContext, DynamicClassDefContext
from mypy.semanal import SemanticAnalyzer
from mypy.typeanal import TypeAnalyser
from mypy.types import (
    CallableType,
    Instance,
    ProperType,
    TypeType,
    TypeVarType,
    UnionType,
    get_proper_type,
)
from mypy.types import Type as MypyType

from . import protocols


class Analyzer:
    def __init__(self, make_resolver: protocols.ResolverMaker) -> None:
        self.make_resolver = make_resolver

    def _has_typevars(self, the_type: ProperType) -> bool:
        if isinstance(the_type, TypeType):
            the_type = the_type.item

        if isinstance(the_type, TypeVarType):
            return True

        if not isinstance(the_type, UnionType):
            return False

        return any(self._has_typevars(get_proper_type(item)) for item in the_type.items)

    def analyze_type(
        self, ctx: AnalyzeTypeContext, annotation: protocols.KnownAnnotations
    ) -> MypyType:
        """
        We resolve annotations at this point. Unless the type being analyzed involves type vars.

        Resolving type vars requires we wait until we are analyzing method/function calls. Between now
        and then we replace the type with an unbound type that wraps a resolved instance because when we
        can resolve the type vars we can't resolve what the type var actually is!
        """
        args = ctx.type.args
        if len(args) != 1:
            ctx.api.fail("Concrete annotations must contain exactly one argument", ctx.context)
            return ctx.type

        model_type = get_proper_type(ctx.api.analyze_type(args[0]))

        def cur_mod_id() -> str:
            # We have to know that ctx.api is TypeAnalyser to know what the current module is
            assert isinstance(ctx.api, TypeAnalyser)
            assert isinstance(ctx.api.api, SemanticAnalyzer)
            return ctx.api.api.cur_mod_id

        if cur_mod_id() == "extended_mypy_django_plugin.annotations":
            # We don't want to resolve the Concrete annotation where it's defined!
            return ctx.type

        resolver = self.make_resolver(ctx=ctx)

        if self._has_typevars(model_type):
            # We don't have the information to resolve type vars at this point
            # We wrap the result so that we can continue this later without mypy
            # being sad about how Concrete doesn't match what we resolve it to in the end
            wrapped = resolver.rewrap_concrete_type(model_type=model_type, annotation=annotation)
            return ctx.type if wrapped is None else wrapped

        resolved = resolver.resolve(annotation, model_type)
        if resolved is None:
            return ctx.type
        else:
            return resolved

    def transform_cast_as_concrete(self, ctx: DynamicClassDefContext) -> None:
        if len(ctx.call.args) != 1:
            ctx.api.fail("Concrete.cast_as_concrete takes exactly one argument", ctx.call)
            return None

        first_arg = ctx.call.args[0]
        if not isinstance(first_arg, NameExpr):
            # It seems too difficult to support anything more complicated from this hook
            ctx.api.fail(
                "cast_as_concrete can only take variable names."
                " Create a variable with what you're passing in and pass in that variable instead",
                ctx.call,
            )
            return None

        node = ctx.api.lookup_qualified(first_arg.name, ctx.call)
        if not node or not node.node or not (arg_type := getattr(node.node, "type", None)):
            ctx.api.fail(
                f'Failed to find a model type represented by "{first_arg.name}"', ctx.call
            )
            return None

        arg_node_typ: ProperType = get_proper_type(arg_type)

        is_type: bool = False
        if isinstance(arg_node_typ, TypeType):
            is_type = True
            arg_node_typ = arg_node_typ.item

        if not isinstance(arg_node_typ, Instance | UnionType | TypeVarType):
            ctx.api.fail(
                f"Expected first argument to Concrete.cast_as_concrete to have a type referencing a model, got {type(arg_node_typ)}",
                ctx.call,
            )
            return None

        # We need much more than is on the interface unfortunately
        assert isinstance(ctx.api, SemanticAnalyzer)
        sem_api = ctx.api

        # The only type var we support is Self
        if isinstance(arg_node_typ, TypeVarType):
            func = sem_api.scope.function
            if func is None or arg_node_typ.name != "Self":
                ctx.api.fail(
                    f"Resolving type variables for cast_as_concrete only implement for the Self type: {arg_node_typ}",
                    ctx.call,
                )
                return

            replacement: Instance | TypeType | None = ctx.api.named_type_or_none(
                func.info.fullname
            )
            if not replacement:
                # This is one of those "no possible to reach in practise" branches
                # because mypy fails before we get here anyways
                ctx.api.fail("The Self type only makes sense on class methods", ctx.call)
                return None

            arg_node_typ = replacement
            if is_type:
                replacement = TypeType(replacement)

            # Need to convince mypy that we can change the type of the first argument
            if isinstance(func.type, CallableType):
                if func.type.arg_names[0] == ctx.name:
                    # Avoid getting an assignment error trying to assign a union of the concrete types to
                    # a variable typed in terms of Self
                    func.type.arg_types[0] = replacement

        concrete_type = self.make_resolver(ctx=ctx).resolve(
            protocols.KnownAnnotations.CONCRETE,
            TypeType(arg_node_typ) if is_type else arg_node_typ,
        )
        if not concrete_type:
            # resolve will already have made a failure if necessary
            return None

        # Perform a cast!
        ctx.call.analyzed = CastExpr(first_arg, concrete_type)
        ctx.call.analyzed.line = ctx.call.line
        ctx.call.analyzed.column = ctx.call.column
        ctx.call.analyzed.accept(sem_api)

        return None

    def transform_type_var_classmethod(self, ctx: DynamicClassDefContext) -> None:
        if len(ctx.call.args) != 2:
            ctx.api.fail("Concrete.type_var takes exactly two arguments", ctx.call)
            return None

        # We need much more than is on the interface unfortunately
        assert isinstance(ctx.api, SemanticAnalyzer)
        sem_api = ctx.api

        inside: str | None = None
        if ctx.api.scope.classes and ctx.api.scope.functions:
            inside = "method scope"
        elif ctx.api.scope.classes:
            inside = "class scope"
        elif ctx.api.scope.functions:
            inside = "function scope"

        if inside:
            # We modify the module scope in this hook, so make sure it's in module scope!
            ctx.api.fail(
                f"Can only use Concrete.type_var at module scope, rather than {inside}", ctx.call
            )
            return None

        # This copies what mypy does to resolve TypeVars
        # https://github.com/python/mypy/blob/v1.10.1/mypy/semanal.py#L4234
        name = sem_api.extract_typevarlike_name(
            AssignmentStmt([NameExpr(ctx.name)], ctx.call.callee), ctx.call
        )
        if name is None:
            return None

        second_arg = ctx.call.args[1]
        parent_type = get_proper_type(sem_api.expr_to_analyzed_type(second_arg))

        if not isinstance(parent_type, Instance):
            if ctx.api.final_iteration:
                ctx.api.fail(f"Failed to locate the model provided: {ctx.name}", ctx.call)
            else:
                ctx.api.defer()

            return None

        type_var_expr = self.make_resolver(ctx=ctx).type_var_expr_for(
            model=parent_type.type,
            name=name,
            fullname=f"{ctx.api.cur_mod_id}.{name}",
            object_type=ctx.api.named_type("builtins.object"),
        )

        # Note that we will override even if we've already generated the type var
        # because it's possible for a first pass to have no values but a second to do have values
        # And in between that we do need this to be a typevar expr
        module = ctx.api.modules[ctx.api.cur_mod_id]
        module.names[name] = SymbolTableNode(GDEF, type_var_expr, plugin_generated=True)
        return None
