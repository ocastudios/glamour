#!/bin/bash

find -type f -name "*.py">lista.tmp;
xgettext --language=Python --keyword=t --output=locale/template.pot -f lista.tmp;
rm lista.tmp;
