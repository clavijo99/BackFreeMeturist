init:
	test -n "$(name)"
	rm -rf ./.git
	find ./ -type f -exec perl -pi -e 's/free-meturist-back/$(name)/g' *.* {} \;
	mv ./free-meturist-back ./$(name)

superuser:
	docker exec -it free-meturist-back ./manage.py createsuperuser

shell:
	docker exec -it free-meturist-back ./manage.py shell

makemigrations:
	docker exec -it free-meturist-back ./manage.py makemigrations

migrate:
	docker exec -it free-meturist-back ./manage.py migrate

initialfixture:
	docker exec -it free-meturist-back ./manage.py loaddata initial

testfixture:
	docker exec -it free-meturist-back ./manage.py loaddata test

test:
	docker exec -it free-meturist-back ./manage.py test

statics:
	docker exec -it free-meturist-back ./manage.py collectstatic --noinput

makemessages:
	docker exec -it free-meturist-back django-admin makemessages

compilemessages:
	docker exec -it free-meturist-back django-admin compilemessages
