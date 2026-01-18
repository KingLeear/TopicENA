# ena_example.R
library(rENA)





# load example dataset from rENA
# data = rENA::RS.data
data <- read.csv("../outputs/topic_keywords_0.05_reflection.csv") # Leet paper



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
groups = c("HDSE", "LDSE")



set.ena = ena(
  data = data,
  units = unitCols,
  codes = codesCols,
  conversation = conversationCols,
  window.size.back = 5,
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
#   groups = c("HDSE","LDSE"),
#   mean = FALSE,
#   center.align.to.origin = FALSE
# )
# 












hdse.lineweights = as.matrix(set.ena$line.weights$Condition$HDSE)
ldse.lineweights = as.matrix(set.ena$line.weights$Condition$LDSE)


hdse.mean = as.vector(colMeans(hdse.lineweights))
ldse.mean = as.vector(colMeans(ldse.lineweights))


ena.plot(set.ena, title = "HDSE mean plot") |>
  ena.plot.network(network = hdse.mean, colors = c("red"))

ena.plot(set.ena, title = "LDSE mean plot") |>
  ena.plot.network(network = ldse.mean, colors = c("blue"))


subtracted.mean = hdse.mean - ldse.mean

ena.plot(
  set.ena,
  title = "Subtracted: HDSE (red) - LDSE (blue)"
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
                   groups = c("HDSE","LDSE"),
                   subtractionMultiplier = 5)




ena_first_points_d1 = as.matrix(set.ena$points$Condition$HDSE)[,1]
ena_second_points_d1 = as.matrix(set.ena$points$Condition$LDSE)[,1]
ena_first_points_d2 = as.matrix(set.ena$points$Condition$HDSE)[,2] 
ena_second_points_d2 = as.matrix(set.ena$points$Condition$LDSE)[,2]
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
