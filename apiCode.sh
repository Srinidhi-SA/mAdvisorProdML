#! /bin/sh
rm -r dist
mkdir dist/
python3 setup.py bdist_egg
ls -l dist/
cp -r dist/* SPARK_DOCKER/marlabs_bi_jobs-0.0.0-py3.6.egg
ls -l SPARK_DOCKER/
cd API-CODE
rm -r mAdvisorProdApiUi
git clone -b main --single-branch https://Srinidhi-SA:Sri160293@github.com/Srinidhi-SA/mAdvisorProdApiUi
cd mAdvisorProdApiUi
rsync -r * ../../SPARK_DOCKER/code/mAdvisor-api/ --exclude API_DOCKER --exclude copyApiFolder.sh --exclude buildspec-oldprod.yml --exclude buildspec-newprod.yml --exclude hadoop_docker --exclude NGINX_DOCKER_NEW_PROD --exclude NGINX_DOCKER_OLD_PROD --exclude copyHadoopImageNewProd.sh --exclude copyHadoopImageOldProd.sh --exclude requirements
cp -r requirements ../../SPARK_DOCKER/requirements/
cp -r static/ ../../SPARK_DOCKER/code/mAdvisor-api/
cd ../../
