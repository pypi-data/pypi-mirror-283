# pypawn-annotation
Python библиотека, реализует автоматическую аннотацию для функций из языка программирования pawn.

- Пример использования модуля. Аннотация к native функции:
```python
import pypawn_annotations

function = pypawn_annotations.PawnFunction(
    string="native bool: function(const iUser, const str: szLogin[32], const str: szPassword[32]);"
)

annotation = pypawn_annotations.Annotation(
    function=function, description=f'Description: {function.name}'
)

print(annotation.show())
```

- Результат выполнения кода
```console
/* 
 * Description: function
 * 
 * @param const int:iUser            iUser
 * @param const str:szLogin[32]      szLogin[32]
 * @param const str:szPassword[32]   szPassword[32]
 * @return                           bool: 
 */
```

**Модуль использует регулярные выражения для поиска групп:**
1. Title: string - ключевое слово, обозначающее что строка является функцией (native, forward, func)
2. General tag: tuple - основной тэг функции, который содержит в себе два элемента:
 	
    - enum объект класса AnnotationTags
 	
    - название тэга
  
3. Name: string - имя функции
4. Args: list[dict] - массив словарей каждый из которых содержит в себе четыре ключа:
 	
    - qualifier: tuple - квалификатор, enum объект класса AnnotationQualifier
 	
    - tag: tuple - работает по принципу general tag
 	
    - name: string - имя аргумента


```console
[0] string: native bool: function(const iUser, const str: szLogin[32], const str: szPassword[32]);
[1] title: native
[2] general_tag: (<AnnotationTags.TAG_CUSTOM: 4>, 'bool:')
[3] name: function
[4] args: [{'qualifier': <AnnotationQualifier.QUALIFIER_CONST: 1>, 'tag': (<AnnotationTags.TAG_INT: 0>, 'int'), 'name': 'iUser', 'description': 'iUser'},
  {'qualifier': <AnnotationQualifier.QUALIFIER_CONST: 1>, 'tag': (<AnnotationTags.TAG_STR: 2>, 'str'), 'name': 'szLogin[32]', 'description': 'szLogin[32]'},
  {'qualifier': <AnnotationQualifier.QUALIFIER_CONST: 1>, 'tag': (<AnnotationTags.TAG_STR: 2>, 'str'), 'name': 'szPassword[32]', 'description': 'szPassword[32]'}]
[5] is_title_tag_function: False
[7] is_title_tag_forward: False
[8] is_title_tag_native: True
```
