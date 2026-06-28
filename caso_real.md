# El caso real: dos cosas que aprendí gobernando el enrutado

Este patrón no salió de un tutorial. Salió de operar un sistema real con varias
decenas de agentes especializados, donde el enrutado tenía que acertar de verdad.
El ecosistema de juguete de este repo (una tienda con ocho agentes) reproduce el
método; las dos lecciones de abajo son las que de verdad costaron.

## Lección 1: un agente nuevo puede quedar invisible

Di de alta un agente nuevo. Funcionaba al probarlo suelto. Pero el orquestador no lo
elegía nunca, ni cuando la petición encajaba con él de lleno.

El motivo: el orquestador no lee a los agentes, lee el **registro**. Y yo había añadido
el agente sin regenerar el registro. Para el enrutado, ese agente no existía.

De ahí la decisión de diseño que ves en este repo: **el registro no se edita a mano, se
genera** (`generar_registro.py`). Y regenerarlo es un paso obligatorio al dar de alta un
agente, no una buena costumbre opcional. Si no, vuelve el agente invisible.

## Lección 2: cuando el enrutador "falla", duda primero del examen

En una de las rondas, dos agentes parecían pisarse: el enrutador mandaba a uno
peticiones que yo creía del otro. Mi primera reacción fue "el registro no discrimina
bien, hay que tocar las descripciones".

Antes de tocar nada, pasé el caso por un revisor independiente con un único encargo:
**intentar demostrar que mi conclusión era falsa**. Y la demostró. El solapamiento no
estaba en el sistema: estaba en cómo yo había escrito las respuestas correctas del banco
de pruebas. El enrutador acertaba; mi examen estaba mal puesto.

La lección: un fallo aparente del enrutador puede ser un fallo de tu evaluación. Por eso el
método de este repo separa dos veredictos distintos: **FALLA** (el sistema se equivoca) y
**HALLAZGO** (tu banco de pruebas o una descripción son ambiguos). Confundirlos te lleva a
"arreglar" lo que no estaba roto.

## Por qué importan las dos juntas

Las dos apuntan a lo mismo: en un sistema multi-agente, el enrutado no se valida mirándolo
una vez y dándolo por bueno. Se valida con un registro que no se desincroniza y con una
evaluación que se cuestiona a sí misma. Eso es lo que este repo intenta enseñar.
