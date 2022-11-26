import random

import faker

fake = faker.Faker(locale='zh_CN')


def fake_article():
    sentenses = fake.texts(nb_texts=10, max_nb_chars=500)
    full_text = ''
    for s in sentenses:
        sf = ''
        for a in s:
            dot = random.choice(['。', '？', '！', '，', '，', '，', '，', '，',
                                '，', '，', '，', '，', '，', '。', '。', '。', '。', '。', '。'])
            if a == '.':
                a = dot
            sf = sf + a
        full_text = full_text + sf
    return full_text.replace('\n', '')


if __name__ == '__main__':
    print(fake_article())
