import faker

fake = faker.Faker(locale='zh_CN')


def fake_article():
    return fake.text(max_nb_chars=500)


if __name__ == '__main__':
    print(fake_article())
