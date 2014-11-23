curl --data "name=Santa 2014" http://127.0.0.1:7171/santatrons
curl -X POST -d "name=Other User&email=alex@gmail.com" http://127.0.0.1:7171/santatrons/1
curl -X POST -d "name=Yet Other User&email=alex@gmail.com" http://127.0.0.1:7171/santatrons/1
curl -X POST -d "name=Alex&email=alex@gmail.com&constraint=2" http://127.0.0.1:7171/santatrons/1
curl -X PUT http://127.0.0.1:7171/santatrons/assign/1