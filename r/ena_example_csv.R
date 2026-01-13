# ena_example.R
library(rENA)





# load example dataset from rENA
# data = rENA::RS.data
data <- read.csv("topic_keywords_0.3.csv")

unitCols = c("Condition", "UserName")

codesCols = c(
  "year.game",
  "space.nasa",
  "israel.israeli",
  "jpeg.file",
  "armenian.armenians",
  "mac.modem"
)

conversationCols = c(
  "Condition",
  "ActivityNumber"
)



groupsVar = "Condition"
groups = c("FirstGame", "SecondGame")



set.ena = ena(
  data = data,
  units = unitCols,
  codes = codesCols,
  conversation = conversationCols,
  window.size.back = 7,
  groupVar = groupsVar,
  groups = groups,
  mean = TRUE
  
)





# ena.plot(set.ena, title = "FirstGame mean plot") |>
#   ena.plot.network(network = first.game.mean, colors = c("red"))
# 
# ena.plot(set.ena, title = "SecondGame mean plot") |>
#   ena.plot.network(network = second.game.mean, colors = c("blue"))
# 
# 
# 
# # Subset lineweights for FirstGame
# first.game.lineweights = as.matrix(set.ena$line.weights$Condition$FirstGame)
# # Subset lineweights for SecondGame
# second.game.lineweights = as.matrix(set.ena$line.weights$Condition$SecondGame)
# 
# first.game.mean = as.vector(colMeans(first.game.lineweights))
# second.game.mean = as.vector(colMeans(second.game.lineweights))
# subtracted.mean = first.game.mean - second.game.mean
# 
# ena.plot(
#   set.ena,
#   title = "Subtracted: FirstGame (red) - SecondGame (blue)"
# ) |>
#   ena.plot.network(
#     network = subtracted.mean * 5,  # optional rescaling
#     colors = c("red", "blue")
#   )
# 
# 
# 
# 
# first.game.points = as.matrix(set.ena$points$Condition$FirstGame)
# 
# ena.plot(set.ena, title = "FirstGame mean network and its points") |>
#   ena.plot.network(network = first.game.mean, colors = c("red")) |>
#   ena.plot.points(points = first.game.points, colors = c("red")) |>
#   ena.plot.group(point = first.game.points, colors =c("red"),
#                  confidence.interval = "box")
# 
# second.game.points = as.matrix(set.ena$points$Condition$SecondGame)
# 
# ena.plot(set.ena, title = "SecondGame mean network and its points") |>
#   ena.plot.network(network = second.game.mean, colors = c("blue")) |>
#   ena.plot.points(points = second.game.points, colors = c("blue")) |>
#   ena.plot.group(point = second.game.points, colors =c("blue"),
#                  confidence.interval = "box")
# 
# 
# ena.plot(set.ena, title = "Subtracted mean network: FirstGame (red) - SecondG
# ame (blue)") |>
#   ena.plot.network(network = subtracted.mean * 5,
#                    colors = c("red", "blue")) |>
#   ena.plot.points(points = first.game.points, colors = c("red")) |>
#   ena.plot.group(point = first.game.points, colors =c("red"),
#                  confidence.interval = "box") |>
#   ena.plot.points(points = second.game.points, colors = c("blue")) |>
#   ena.plot.group(point = second.game.points, colors =c("blue"),
#                  confidence.interval = "box")



#with helper function
plot = ena.plotter(set.ena,
                   points = T,
                   mean = T,
                   network = T,
                   print.plots = T,
                   groupVar = "Condition",
                   groups = c("SecondGame","FirstGame"),
                   subtractionMultiplier = 5)