# ena_example.R
options(repos = c(CRAN = "https://cloud.r-project.org"))
install.packages(c("htmlwidgets", "htmltools", "devtools", "pkgload", "webshot2"))

library(rENA)

# Rscript /Users/owen/Documents/TopicENA/r/example.R /Users/owen/Documents/TopicENA/r/RS.data.rda /Users/owen/Documents/TopicENA/outputs

args <- commandArgs(trailingOnly = TRUE)
in_path <- normalizePath(args[1], mustWork = TRUE)
out_path <- normalizePath(args[2], mustWork = TRUE)
# window_size_back <- normalizePath(args[3], mustWork = TRUE)


data <- read.csv(in_path) # Leet paper
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










outfile  <- file.path(out_path, "ena_plot.png")
# htmlfile <- file.path(out_path, "ena_plot.html")

p = ena.plotter(set.ena,
                   points = T,
                   mean = T,
                   network = T,
                   print.plots = T,
                   groupVar = "Condition",
                   groups = c("high","low"),
                   subtractionMultiplier = 5)


save_ena_html_and_png <- function(p, out_dir=".", prefix="ena",
                                  width=1600, height=1200, zoom=2, delay=1) {

  for (g in names(p$plots)) {
    w <- p$plots[[g]]$plot

    html_file <- file.path(out_dir, sprintf("%s_%s.html", prefix, g))
    png_file  <- file.path(out_dir, sprintf("%s_%s.png",  prefix, g))

    htmlwidgets::saveWidget(
      widget = w,
      file = html_file,
      selfcontained = TRUE
    )

    webshot2::webshot(
      url    = normalizePath(html_file, winslash = "/"),
      file   = png_file,
      vwidth = width,
      vheight = height,
      zoom   = zoom,
      delay  = delay
    )
  }
}  

save_ena_html_and_png(p, out_dir=out_path, prefix="ena",
                      width=1600, height=1200, zoom=2, delay=1.5)

# save_ena_html <- function(p, out_dir = ".", prefix = "ena") {
#   dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

#   for (g in names(p$plots)) {
#     w <- p$plots[[g]]$plot
#     html_file <- file.path(out_dir, sprintf("%s_%s.html", prefix, g))

#     htmlwidgets::saveWidget(
#       widget = w,
#       file = html_file,
#       selfcontained = TRUE
#     )
#   }
# }

# save_ena_html(p, out_dir = out_path, prefix = "ena")

# w <- plot$plot

# libdir <- file.path(dirname(htmlfile), "lib")

# htmlwidgets::saveWidget(
#   widget = w,
#   file = htmlfile,
#   selfcontained = FALSE,
#   libdir = libdir
# )

# # webshot2 需要 headless browser（Chromium/Chrome）
# webshot2::webshot(
#   url    = htmlfile,
#   file   = outfile,
#   vwidth = 1600, vheight = 1200,
#   zoom   = 2
# )

message("Wrote: ", normalizePath(outfile, winslash = "/", mustWork = FALSE))
message("Exists? ", file.exists(outfile))
