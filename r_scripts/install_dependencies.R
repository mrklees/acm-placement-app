# Title     : TODO
# Objective : TODO
# Created by: keyvanm
# Created on: 2019-05-27

chooseCRANmirror(ind=1)  # Set cran to 0-Cloud [https]

packages = c('data.table', 'dplyr', 'readxl', 'tidyr')

for (package in packages) {
    tryCatch({
        library(package, character.only=TRUE)
    }, error = function(e) {
        install.packages(package)
    })
}
