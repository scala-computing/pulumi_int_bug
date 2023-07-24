import sys
import pulumi
import json
from pulumi import Output
from pulumi import automation as auto
from pulumi.dynamic import CreateResult, Resource, ResourceProvider, UpdateResult
from rich import print
from rich.panel import Panel

test_dictionary = {
    "test_int_value": 42,
    "test_float_value": 42.0,
    "test_string_value": "42",
}


class MyResourceProvider(ResourceProvider):
    def create(self, inputs):
        """Show how a value has transformed from an int to a float"""
        test_value = inputs["test_value"]
        test_dictionary = inputs["test_dictionary"]

        if type(test_value) == float:
            print(
                Panel(
                    f""" \n value of test_value is {test_value} \n type of test_value is {type(test_value)} \n expected type of test_value is int""",
                    title="! WARNING !",
                )
            )

        if type(test_dictionary["test_int_value"]) == float:
            print(
                Panel(
                    f""" \n value of test_dictionary["test_int_value"] is {test_dictionary["test_int_value"]} \n type of test_dictionary["test_int_value"] is {type(test_dictionary["test_int_value"])} \n expected type of test_dictionary["test_int_value"] is int""",
                    title="! WARNING !",
                )
            )

        # this case is never hit
        if type(test_dictionary["test_string_value"]) == float:
            print(
                Panel(
                    f""" \n value of test_dictionary["test_string_value"] is {test_dictionary["test_string_value"]} \n type of test_dictionary["test_string_value"] is {type(test_dictionary["test_string_value"])} \n expected type of test_dictionary["test_string_value"] is str""",
                    title="! WARNING !",
                )
            )

        return CreateResult(
            id_="0",
            outs={
                "test_value": test_value,
                "test_value_type": str(type(test_value)),
                "test_dictionary": test_dictionary,
                "test_dictionary_test_int_value_type": str(
                    type(test_dictionary["test_int_value"])
                ),
                "test_dictionary_test_string_value_type": str(
                    type(test_dictionary["test_string_value"])
                ),
            },
        )


class MyResourceProviderInputArgs:
    test_value: pulumi.Input[int]

    def __init__(
        self,
        test_value: pulumi.Input[int],
        test_dictionary: pulumi.Input[dict],
    ) -> None:
        self.test_value = test_value
        self.test_dictionary = test_dictionary


class MyResourceResource(Resource):
    test_value: Output[int]

    def __init__(
        self,
        name: str,
        args: MyResourceProviderInputArgs,
        opts: pulumi.ResourceOptions = None,
    ) -> None:
        super().__init__(MyResourceProvider(), name, vars(args), opts)


def pulumi_program():
    my_resource = MyResourceResource(
        "my-resource",
        MyResourceProviderInputArgs(
            test_value=42,
            test_dictionary=test_dictionary,
        ),
    )

    pulumi.export("test_value", my_resource.test_value)
    pulumi.export("test_dictionary", my_resource.test_dictionary)


stack_name = "test"
project_name = "dynamic_provider_int_bug"

stack = auto.create_or_select_stack(
    stack_name=stack_name, project_name=project_name, program=pulumi_program
)

print("successfully initialized stack")

# set stack configuration specifying the AWS region to deploy
print("setting up config")
stack.set_config("aws:region", auto.ConfigValue(value="us-west-2"))
print("config set")

print("refreshing stack...")
stack.refresh(on_output=print)
print("refresh complete")

destroy = False

args = sys.argv[1:]
if len(args) > 0:
    if args[0] == "destroy":
        destroy = True

if destroy:
    print("destroying stack...")
    stack.destroy(on_output=print)
    print("stack destroy complete")
    sys.exit()


print("updating stack...")
up_res = stack.up(on_output=print)
