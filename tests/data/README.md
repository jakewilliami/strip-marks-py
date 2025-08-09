These (near-complete) test cases were generated using Julia.  Julia's strip marks functionality is based on utf8proc, which is efficient and well-defined.

```julia
using Unicode

Unicode.normalize("...", stripmarks=true)
```
