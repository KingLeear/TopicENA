# ena_example.R
library(rENA)

# Rscript /Users/owen/Documents/TopicENA/r/example.R /Users/owen/Documents/TopicENA/r/RS.data.rda /Users/owen/Documents/TopicENA/outputs
# data(RS.data)

args <- commandArgs(trailingOnly = TRUE)
in_path <- normalizePath(args[1], mustWork = TRUE)
out_path <- normalizePath(args[2], mustWork = TRUE)
load(in_path)
# rs_data_path <- args[1]

# # 載入 RS.data（假設是 .RData 或 .rda）
# load(rs_data_path)


# message("args: ", args[1])





# data(args[1])


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








outfile  <- file.path(out_path, "ena_plot.png")
htmlfile <- file.path(out_path, "ena_plot.html")

p <- plot(enaset) |>
  add_points(Condition$FirstGame, mean = TRUE, colors = "blue") |>
  add_points(Condition$SecondGame, mean = TRUE, colors = "red") |>
  with_means() |>
  add_network() |>
  add_nodes()

w <- p$plot

htmlwidgets::saveWidget(w, htmlfile, selfcontained = TRUE)

webshot2::webshot(
  url    = htmlfile,
  file   = outfile,
  vwidth = 1600, vheight = 1200,
  zoom   = 2
)

message("Wrote: ", normalizePath(outfile, winslash = "/", mustWork = FALSE))
message("Exists? ", file.exists(outfile))
