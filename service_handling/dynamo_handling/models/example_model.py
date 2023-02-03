from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from botocore.session import Session

from config import example_table_name


class ExampleModel(Model):
    class Meta:
        table_name = example_table_name
        billing_mode = "PAY_PER_REQUEST"
        region = Session().get_config_variable('region')
    example_number = NumberAttribute(hash_key=True)
    valence = UnicodeAttribute(range_key=True)

    filename = UnicodeAttribute()
    video_id = UnicodeAttribute()
    emotion_id = NumberAttribute(default=100)


def create():
    # Create the table
    if not ExampleModel.exists():
        ExampleModel.create_table(wait=True)


if __name__ == "__main__":
    create()
