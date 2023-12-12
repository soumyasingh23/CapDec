import pickle, json

kagle_json = 'annotations/dataset_flickr8k.json'
new_json_train = 'post_processed_karpthy/train.json'
new_json_test = 'post_processed_karpthy/test.json'
new_json_val = 'post_processed_karpthy/val.json'


def map_format_kaggle_to_clipcap():
    def extract_imgid_from_name(filename):
        return str(int(filename.split('.')[0].split('_')[0]))

    with open(kagle_json) as f:
        kaggle_data = json.load(f)
    train_data = []
    test_data = []
    val_data = []
    splits = {'train': train_data, 'test': test_data, 'val': val_data, 'restval': train_data}
    out_names = {'train': new_json_train, 'test': new_json_test, 'val': new_json_val}
    for img in kaggle_data['images']:
        imgid = extract_imgid_from_name(img['filename'])
        for cap in img['sentences']:
            correct_format = {"image_id": int(imgid), "caption": cap['raw'], "id": int(cap['sentid']), "filename":img['filename']}
            splits[img['split']].append(correct_format)

    DBG = False
    if not DBG:
        for name in out_names:
            with open(out_names[name], 'w') as f:
                json.dump(splits[name], f)

        for name in out_names:
            with open(out_names[name][:-5] + '_metrics_format.json', 'w') as f:
                annos = splits[name]
                ids = [{"id": int(a["image_id"])} for a in annos]
                final = {"images": ids, "annotations": annos}
                json.dump(final, f)

    if DBG:
        # rons annotations
        with open('annotations/dataset_flickr8k.json') as f:
        # with open('../../train_caption.json') as f:
            cur_data = json.load(f)
        ids = [str(int(c['image_id'])) for c in cur_data]
        new_ids = [str(int(c['image_id'])) for c in train_data]
        ids.sort()  # inplace
        new_ids.sort()
        assert ids == new_ids
        print('OK')


if __name__ == '__main__':
    map_format_kaggle_to_clipcap()