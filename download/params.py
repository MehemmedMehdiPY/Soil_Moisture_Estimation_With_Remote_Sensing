from sentinelhub import DataCollection

def get_params(sentinel='sentinel_1'):

    if sentinel.lower().strip() == 'sentinel_1':
        data_collection = DataCollection.SENTINEL1
        img_eval = """
//VERSION=3

function evaluatePixel(sample) {
     return [
        65535* sample.VV,
        65535* sample.VH
        ];
}

function setup() {
  return {
    input: [{
      bands: [
        "VV",
        "VH"
      ]
    }],
    output: {
      bands: 2,
      sampleType: "UINT16"
    }
  }
}
"""

    elif sentinel.lower().strip() == 'sentinel_2':
        data_collection = DataCollection.SENTINEL2_L2A
        img_eval = """
//VERSION=3

function evaluatePixel(sample) {
     return [
        65535* sample.B02,
        65535* sample.B03,
        65535* sample.B04,
        65535* sample.B08,
        65535* sample.B8A,
        65535* sample.B11,
        ];
}

function setup() {
  return {
    input: [{
      bands: [
        "B02",
        "B03",
        "B04",
        "B08",
        "B8A",
        "B11",
      ]
    }],
    output: {
      bands: 6,
      sampleType: "UINT16"
    }
  }
}
"""

    else:
        raise ValueError('Wrong sentinel name {}. Input sentinel_1 or sentinel_2, instead'.format(sentinel))
  
    return img_eval, data_collection