# xFDS Logo

## Setting up the mesh

The [xFDS](https://xfds.pbd.tools) logo was built using the blocks in FDS to create a pixelated font. To make this simple, each block was 1m x 1m x 1m. The `zmin` bound could be altered to play with the depth of field creating a shadow effect. In setting up the &MESH, the `zmin` is filterd through a built-in absolute value function to ensure it is positive.

```lua
&MESH XB=0, 27, 0, 11, {{ zmin }}, 0, IJK=27, 11, {{ zmin|abs }}/
```

## Opening the Mesh Boundaries

Since the mesh boundaries default to `'INERT'`, they were removed so the color didn't show. The following snippet loops through each mesh boudary and assign it to `'OPEN'`.

```lua
{% for bound in ['XMIN', 'XMAX', 'YMIN', 'YMAX', 'ZMIN', 'ZMAX']%}
&VENT MB='{{ bound }}', SURF_ID='OPEN'/
{% endfor %}
```

Which yields the following:
```lua
&VENT MB='XMIN', SURF_ID='OPEN'/
&VENT MB='XMAX', SURF_ID='OPEN'/
&VENT MB='YMIN', SURF_ID='OPEN'/
&VENT MB='YMAX', SURF_ID='OPEN'/
&VENT MB='ZMIN', SURF_ID='OPEN'/
&VENT MB='ZMAX', SURF_ID='OPEN'/
```

## Setting up the &OBSTs

The &OBSTs were intended to be orange blocks with a black outline. A macro was defined
in the FDS file to do the following:
- Generate two &OBST records, one solid orange, and one in black outline.
- Specify the width/height rather than maximum dimension by using `{{ x0 }}, {{ x0 + dx }}, {{ y0 }}, {{ y0 + dy }}` for the x and y dimensions. If an &OBST needs to move in a given direction, it can move without having to reacalculate the new maximum dimension.
- `{%+ if mult %}MULT_ID='{{ mult }}', {% endif %}` Will include the `MULT_ID` parameter if one is defined. This is needed for the diagonals in the `x`.



The following macro...

```lua
{% macro obst(x0, y0, dx=1, dy=1, mult='') -%}
&OBST XB= {{ x0 }}, {{ x0 + dx }}, {{ y0 }}, {{ y0 + dy }}, -1, 0,
      {%+ if mult %}MULT_ID='{{ mult }}', {% endif %}SURF_ID='SOLID'/
&OBST XB= {{ x0 }}, {{ x0 + dx }}, {{ y0 }}, {{ y0 + dy }}, {{ zmin }}, 0,
      {%+ if mult %}MULT_ID='{{ mult }}', {% endif %}SURF_ID='OUTLINE', OUTLINE=.TRUE./
{%- endmacro -%}
```

... allows you to call ...

```lua
{{ obst(x0=0, y0=0, dy=5) }}
```

... to generate the following FDS lines:

```lua
&OBST XB= 0, 1, 0, 5, -1, 0,
      SURF_ID='SOLID'/
&OBST XB= 0, 1, 0, 5, -2, 0,
      SURF_ID='OUTLINE', OUTLINE=.TRUE./
```

To shift both &OBST lines up so `XMIN = 5`, the `x0` parameter can be adjsted so ...

```lua
{{ obst(x0=5, y0=0, dy=5) }}
```

... becomes ...

```lua
&OBST XB= 5, 6, 0, 5, -1, 0,
      SURF_ID='SOLID'/
&OBST XB= 5, 6, 0, 5, -2, 0,
      SURF_ID='OUTLINE', OUTLINE=.TRUE./
```
