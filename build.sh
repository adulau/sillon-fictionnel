#!/bin/bash

hugo
rsync --include ".*" -v -rz --checksum public/ ubuntu@illich.paperbay.org:/var/www/sillon-fictionnel.club
