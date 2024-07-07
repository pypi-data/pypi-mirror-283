Syntax
======

.. toctree::

Notes
-----

The function ``raw_c(str)`` inserts that str into the transpiled C++.

Importing replaces dots (``.``) with slashes (``/``), for example:
::

    import custom.random
    from custom.random import *
    from custom.random import a

Any of these lines would import the '``random``' module in the '``~/.local/lib/pyg3a/custom``' folder.
Variables are statically typed.
PyG3A will try and infer types, but it is recommended that you use type hints where possible. Function argument types are not inferred and must be specified.

Syntax Support
--------------

===============  ===============  =================================
    Keyword          Support                 Explanation
===============  ===============  =================================
def              Supported
return           Supported
=                Supported
:=               Supported
(operator)=      Supported
tuple unpacking  Supported
while            Supported
for              Supported
if               Supported
elif             Supported
else             Supported
import           Supported
from             Supported
pass             Supported
break            Supported
continue         Supported
lambda           Supported
a if b else c    Supported
{set}            Supported
a.b              Supported
(tuple)          Supported
[list]           Supported
and              Supported
or               Supported
\+               Supported
\-               Supported
\*               Supported
/                Supported
//               Supported
%                Supported
\*\*             Supported
<<               Supported
>>               Supported
\\               Supported
^                Supported
&                Supported
~                Supported
not              Supported
==               Supported
<                Supported
<=               Supported
>                Supported
\>=              Supported
is               Supported
is not           Supported
del              Supported
match            Support Planned
type             Support Planned
class            Support Planned
f"strings"       Support Planned
[sli:ces]        Support Planned
a for b in c     Support Planned
@decorator       Support Planned
def func[T]      Support Planned
async            No Support       no async support in c++
await            No Support       no async support in c++
with             No Support       no error support in libfxcg
raise            No Support       no error support in libfxcg
assert           No Support       no error support in libfxcg
try/except       No Support       no error support in libfxcg
global           No Support       automatically used in c++
nonlocal         No Support       no nested function support in c++
dict             No Support       would be annoying to write
yield            No Support       no generator support in c++
matrix @ matrix  No Support       little use case
===============  ===============  =================================
