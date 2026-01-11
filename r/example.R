# ena_example.R
library(rENA)

data(RS.data)

codenames <- c(
  "Data",
  "Technical.Constraints",
  "Performance.Parameters",
  "Client.and.Consultant.Requests",
  "Design.Reasoning",
  "Collaboration"
)

units   <- c("Condition", "UserName")
horizon <- c("Condition", "GroupName")

enaset <- RS.data |>
  accumulate(units, codenames, horizon) |>
  ena.make.set()

# outfile <- "ena_plot.png"
outfile <- file.path(getwd(), "ena_plot.png")

png(filename = outfile, width = 1600, height = 1200, res = 200)
on.exit(dev.off(), add = TRUE)

p <- plot(enaset) |>
  add_points(Condition$FirstGame, mean = TRUE, colors = "blue") |>
  add_points(Condition$SecondGame, mean = TRUE, colors = "red") |>
  with_means() |>
  add_network() |>
  add_nodes()

print(p)


message("Wrote: ", normalizePath(outfile, winslash = "/", mustWork = FALSE))
message("Exists? ", file.exists(outfile))
