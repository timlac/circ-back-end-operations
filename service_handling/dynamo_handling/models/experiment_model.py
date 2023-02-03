from pynamodb.models import Model
from pynamodb.indexes import LocalSecondaryIndex, AllProjection
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, ListAttribute
from botocore.session import Session

from config import experiment_table_name


class ProcessedIndex(LocalSecondaryIndex):
    """
    This class represents a local secondary index
    """
    class Meta:
        # All attributes are projected
        projection = AllProjection()
    alias = UnicodeAttribute(hash_key=True)
    processed_status = NumberAttribute(range_key=True)


class ExperimentModel(Model):
    class Meta:
        table_name = experiment_table_name
        billing_mode = "PAY_PER_REQUEST"
        region = Session().get_config_variable('region')
    alias = UnicodeAttribute(hash_key=True)
    filename = UnicodeAttribute(range_key=True)
    video_id = UnicodeAttribute()
    emotion_id = NumberAttribute(default=100)
    processed_status = NumberAttribute(default=0)
    valence = UnicodeAttribute()
    emotion_id_reply = NumberAttribute(default=100)
    emotion_options = ListAttribute(of=NumberAttribute)

    processed_index = ProcessedIndex()


def create():
    # Create the table
    if not ExperimentModel.exists():
        ExperimentModel.create_table(wait=True)


if __name__ == "__main__":
    create()
