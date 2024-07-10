from keras.optimizers import Adam
from keras.utils import get_custom_objects

from seg_tgce.data.crowd_seg import get_all_data
from seg_tgce.layers import SparseSoftmax
from seg_tgce.loss.tgce import TcgeConfig, TcgeSs
from seg_tgce.models.unet import unet_tgce

TARGET_IMG_SHAPE = (128, 128)


def main() -> None:
    train, val, test = get_all_data(batch_size=8, with_sparse_data=False)
    # val.visualize_sample(batch_index=138, sample_indexes=[2, 3, 4, 5])
    print(f"Train: {len(train)} batches, {len(train) * train.batch_size} samples")
    print(f"Val: {len(val)} batches, {len(val) * val.batch_size} samples")
    print(f"Test: {len(test)} batches, {len(test) * test.batch_size} samples")

    get_custom_objects()["sparse_softmax"] = SparseSoftmax()

    model = unet_tgce(
        input_shape=TARGET_IMG_SHAPE + (3,),
        out_channels=train.n_classes,
        n_scorers=train.n_scorers,
        out_act_functions=("sparse_softmax", "sparse_softmax"),
        name="UNET-TGCE",
    )

    model.compile(
        loss=TcgeSs(
            q=0.01,
            config=TcgeConfig(
                num_annotators=train.n_scorers, num_classes=train.n_classes
            ),
        ),
        optimizer=Adam(),
    )
    model.fit(train, validation_data=val, epochs=1)


main()
