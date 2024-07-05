Maintaining this Package
1) Implement changes on main or any branch derived from main
2) Merge derived branch with finished changes back to main
3) Push to main in order to provide new state to other devs and to trigger test suite run
4) Merge main to release branch
5) Once all changes of a realese are finished, on release branch bump version number via `poetry version patch`
6) Push to release in order to trigger test suite run and publish the new version to pypi.org
7) Merge release back to main in order to sync the version number


Note to myself: Don't create a root folder by hand in which you call poetry new <package name> -> this will lead to one extra leveled root that you don't want.
e.g.: sir_utilites/sir_utilites/sir_utilites - simply call poetry new where you want your new package to live (for example among other packages in a folder called python_packages)