# ena_example.R
library(rENA)





# load example dataset from rENA
# data = rENA::RS.data
data <- read.csv("../demo/topic_keywords_asap_0.01_reflection.csv") # Leet paper



unitCols = c("Condition", "UserName")

headers <- colnames(data)
codesCols <- setdiff(
  headers,
  c("Condition", "ActivityNumber", "UserName", "text")
)

conversationCols = c(
  "Condition",
  "ActivityNumber"
)



groupsVar = "Condition"
groups = c("high", "low")



set.ena = ena(
  data = data,
  units = unitCols,
  codes = codesCols,
  conversation = conversationCols,
  window.size.back = 20,
  groupVar = groupsVar,
  groups = groups,
  mean = TRUE
)

# set.ena = ena(
#   data = data,
#   units = unitCols,
#   codes = codesCols,
#   conversation = conversationCols,
#   window.size.back = 2,
#   groupVar = groupsVar,
#   groups = c("high","low"),
#   mean = FALSE,
#   center.align.to.origin = FALSE
# )
# 












high.lineweights = as.matrix(set.ena$line.weights$Condition$high)
low.lineweights = as.matrix(set.ena$line.weights$Condition$low)


high.mean = as.vector(colMeans(high.lineweights))
low.mean = as.vector(colMeans(low.lineweights))


ena.plot(set.ena, title = "high mean plot") |>
  ena.plot.network(network = high.mean, colors = c("red"))

ena.plot(set.ena, title = "low mean plot") |>
  ena.plot.network(network = low.mean, colors = c("blue"))


subtracted.mean = high.mean - low.mean

ena.plot(
  set.ena,
  title = "Subtracted: high (red) - low (blue)"
) |>
  ena.plot.network(
    network = subtracted.mean * 5,  # optional rescaling
    colors = c("red", "blue")
  )










#with helper function
plot = ena.plotter(set.ena,
                   points = T,
                   mean = T,
                   network = T,
                   print.plots = T,
                   groupVar = "Condition",
                   groups = c("high","low"),
                   subtractionMultiplier = 5)




ena_first_points_d1 = as.matrix(set.ena$points$Condition$high)[,1]
ena_second_points_d1 = as.matrix(set.ena$points$Condition$low)[,1]
ena_first_points_d2 = as.matrix(set.ena$points$Condition$high)[,2] 
ena_second_points_d2 = as.matrix(set.ena$points$Condition$low)[,2]
t_test_d1 = t.test(ena_first_points_d1, ena_second_points_d1)
t_test_d2 = t.test(ena_first_points_d2, ena_second_points_d2)
t_test_d1
t_test_d2


mean(ena_first_points_d1)
mean(ena_second_points_d1)
mean(ena_first_points_d2)
mean(ena_second_points_d2)
sd(ena_first_points_d1)
sd(ena_second_points_d1)
sd(ena_first_points_d2)
sd(ena_second_points_d2)
length(ena_first_points_d1)
length(ena_second_points_d1)
length(ena_first_points_d2)
length(ena_second_points_d2)
