fuel_dine
==============================

__Version:__ 0.1.0

Decide where the team should dine in the restaurant.

The API `docs` are available at [docs](http://localhost:8000/docs) once the server is running locally.

There is a front-end app for demonstration purpose. The App is refactored to use AJAX requests.

**Note**: You need to set up the `GOOGLE_SERVICES_API_KEY` in environment
variables for adding restaurants through geocoding and reverse geocoding
functionality. [Generate your API key here](https://developers.google.com/maps/documentation/geolocation/get-api-key).

The features of the app are:

 - Ability to add restaurant based on geo-coding and reverse geo-coding.
 - Keep a track of visited restaurants by user.
 - Ability to read/write reviews. A special symbol is displayed if it's your own review.
 - Ability to comment on reviews.
 - Ability to thumbs down a restaurant. The restaurant that is thumbs down would not appear in listing or results for the user.
 - User model is extended as profile to add more functionality.
 - REST API that can be integrated with any external service.
 
The tests can be run via `py.test` that tests various API end-points.

TODO
----

- The current app use `BasicAuthentication`. The Authentication and Authorization still needs to be improved.
- The ability to reset vote counter for all restaurants and for all users.
    - Currently this is time consuming and removed from the app.
    An [issue is created on django-vote](https://github.com/shanbay/django-vote/issues/53)
    to know the best alternative for this extra feature.
- Several improvements are needed in the UI.
    - On restaurant detail page, rather than JS alerts, a better way is needed to depict success and errors.
    - Visual representation needed for the icons (in case user already visited/voted/thumbs down a restaurant).
    - DOM manipulation method needs to be improved.


## Getting up and running

Minimum requirements: **pip, fabric, python3 & [postgres][install-postgres]**, setup is tested on Mac OSX only.

```
brew install postgres python3
[sudo] pip install fabric
```

[install-postgres]: http://www.gotealeaf.com/blog/how-to-install-postgresql-on-a-mac

In your terminal, type or copy-paste the following:

    git clone git@github.com:CuriousLearner/fuel-dine-web.git; cd fuel-dine-web; fab init

Go grab a cup of coffee, we bake your hot development machine.

Useful commands:

- `fab serve` - start [django server](http://localhost:8000/)
- `fab deploy_docs` - deploy docs to server
- `fab test` - run the test locally with ipdb

**NOTE:** Checkout `fabfile.py` for all the options available and what/how they do it.


## Deploying Project

The deployment are managed via travis, but for the first time you'll need to set the configuration values on each of the server.

Check out detailed server setup instruction [here](docs/backend/server_config.md).

## How to release fuel_dine

Execute the following commands:

```
git checkout master
fab test
bumpversion patch  # 'patch' can be replaced with 'minor' or 'major'
git push origin master
git push origin master --tags
git checkout qa
git rebase master
git push origin qa
```

## Contributing

Golden Rule:

> Anything in **master** is always **deployable**.

Avoid working on `master` branch, create a new branch with meaningful name, send pull request asap. Be vocal!

Refer to [CONTRIBUTING.md][contributing]

[contributing]: http://github.com/CuriousLearner/fuel-dine-web/tree/master/CONTRIBUTING.md
