all:webpage/public/index.html pladmin/pltplconf/templates/pltplconf/index.html

webpage/public/index.html:webpage/page webpage/package.json webpage/tsconfig.json webpage/webpack.config.js
	cd webpage && npm run build

pladmin/pltplconf/templates/pltplconf/index.html:webpage/public/index.html
	rm -rf pladmin/pltplconf/templates && mkdir -p pladmin/pltplconf/templates && rm -rf pladmin/pltplconf/static && cp -r webpage/public pladmin/pltplconf/templates/pltplconf && mv pladmin/pltplconf/templates/pltplconf/static pladmin/pltplconf/static && python3 replace_static.py pladmin/pltplconf/templates/pltplconf/index.html

.PHONLY:clean
clean:
	rm -fr webpage/public && rm -rf pladmin/pltplconf/templates/pltplconf && rm -rf 




