#!/bin/bash
#
# Gera arquivo template.pot para ser usado na tradução de programas
#
#Uso: 
#1- salve este arquivo na pasta que contém seu código;
#2- execute este arquivo;
#3- informe a extensão dos arquivos que você quer varrer para gerar o arquivo template.pot;
#   a extensão deve ser informada sem o ponto, como em py ou sh

echo "Para que extensão você quer gerar o arquivo template.pot?";
read EXTENSAO;
echo "vou procurar por arquivos com a extensão "$EXTENSAO;
find -type f -name "*.$EXTENSAO" > lista.tmp;
echo "encontrei os seguintes arquivos:";
cat lista.tmp;
mkdir locale;
xgettext --language=Python --keyword=t --output=locale/template.pot -f lista.tmp;

rm lista.tmp;

echo "Foi criada a pasta locale e dentro dela o arquivo template.pot";
