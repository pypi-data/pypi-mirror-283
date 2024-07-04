BASE_RIG_TFORM = dict(
    {
        "Transform": ["EulerTransform"],
        "NumberOfParameters": ["3"],
        "TransformParameters": ["0", "0", "0"],
        "InitialTransformParametersFileName": ["NoInitialTransform"],
        "HowToCombineTransforms": ["Compose"],
        "FixedImageDimension": ["2"],
        "MovingImageDimension": ["2"],
        "FixedInternalImagePixelType": ["float"],
        "MovingInternalImagePixelType": ["float"],
        "Size": ["0", "0"],
        "Index": ["0", "0"],
        "Spacing": ["", ""],
        "Origin": ["0.0000", "0.0000"],
        "Direction": [
            "1.0000000000",
            "0.0000000000",
            "0.0000000000",
            "1.0000000000",
        ],
        "UseDirectionCosines": ["true"],
        "CenterOfRotationPoint": ["0", "0"],
        "ResampleInterpolator": ["FinalNearestNeighborInterpolator"],
        "Resampler": ["DefaultResampler"],
        "DefaultPixelValue": ["0.000000"],
        "ResultImageFormat": ["mha"],
        "ResultImagePixelType": ["float"],
        "CompressResultImage": ["true"],
    }
)

BASE_TRANSLATION_TFORM = dict(
    {
        "Transform": ["TranslationTransform"],
        "NumberOfParameters": ["2"],
        "TransformParameters": ["0", "0"],
        "InitialTransformParametersFileName": ["NoInitialTransform"],
        "HowToCombineTransforms": ["Compose"],
        "FixedImageDimension": ["2"],
        "MovingImageDimension": ["2"],
        "FixedInternalImagePixelType": ["float"],
        "MovingInternalImagePixelType": ["float"],
        "Size": ["0", "0"],
        "Index": ["0", "0"],
        "Spacing": ["", ""],
        "Origin": ["0.0000", "0.0000"],
        "Direction": [
            "1.0000000000",
            "0.0000000000",
            "0.0000000000",
            "1.0000000000",
        ],
        "UseDirectionCosines": ["true"],
        "CenterOfRotationPoint": ["0", "0"],
        "ResampleInterpolator": ["FinalNearestNeighborInterpolator"],
        "Resampler": ["DefaultResampler"],
        "DefaultPixelValue": ["0.000000"],
        "ResultImageFormat": ["mha"],
        "ResultImagePixelType": ["float"],
        "CompressResultImage": ["true"],
    }
)


BASE_AFF_TFORM = dict(
    {
        "Transform": ["AffineTransform"],
        "NumberOfParameters": ["6"],
        "TransformParameters": ["1", "0", "0", "1", "0", "0"],
        "InitialTransformParametersFileName": ["NoInitialTransform"],
        "HowToCombineTransforms": ["Compose"],
        "FixedImageDimension": ["2"],
        "MovingImageDimension": ["2"],
        "FixedInternalImagePixelType": ["float"],
        "MovingInternalImagePixelType": ["float"],
        "Size": ["0", "0"],
        "Index": ["0", "0"],
        "Spacing": ["0", "0"],
        "Origin": ["0.0000", "0.0000"],
        "Direction": [
            "1.0000000000",
            "0.0000000000",
            "0.0000000000",
            "1.0000000000",
        ],
        "UseDirectionCosines": ["true"],
        "CenterOfRotationPoint": ["0", "0"],
        "ResampleInterpolator": ["FinalNearestNeighborInterpolator"],
        "Resampler": ["DefaultResampler"],
        "DefaultPixelValue": ["0.000000"],
        "ResultImageFormat": ["mha"],
        "ResultImagePixelType": ["float"],
        "CompressResultImage": ["true"],
    }
)
