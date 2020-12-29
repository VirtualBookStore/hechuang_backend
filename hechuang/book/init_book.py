
def init_book(apps, schema_editor):
    Book: type = apps.get_model('book', 'Book')

    se_book = Book.objects.create(isbn='7111548973',
                               title='软件工程',
                               description='实践者的研究方法',
                               price=9900,
                               new_total=5,
                               tag='教科书 软件工程'
                               )
    java_pl_book = Book.objects.create(isbn='7302244752',
                                    title='Java程序设计',
                                    description='Java程序设计',
                                    price=3500,
                                    new_total=0,
                                    old_total=5,
                                    recommended=True,
                                    tag='教科书 Java')
    core_java_book = Book.objects.create(isbn='7115420114',
                                         title='Java核心技术',
                                         description='Core Java',
                                         price=10900,
                                         new_total=10,
                                         old_total=10,
                                         recommended=False,
                                         tag='Java')



