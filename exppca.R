library(logisticPCA)
args = commandArgs(trailingOnly=TRUE)

my_data <- read.csv(args[1])
if (args[3] == 'logisticPCA') {
    model = logisticPCA(my_data, k = as.integer(args[4]), m = as.integer(args[5]))
} else if (args[3] == 'logisticSVD') {
    model = logisticSVD(my_data, k = as.integer(args[4]))
}
fn <- sprintf("%s.rda", args[2])
save(model, file = fn) 