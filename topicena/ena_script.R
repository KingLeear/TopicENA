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
  c("Condition", "ActivityNumber", "UserName", "text", "doc_id")
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



message("Wrote: ", normalizePath(outfile, winslash = "/", mustWork = FALSE))
message("Exists? ", file.exists(outfile))


# ena_first_points_d1 = as.matrix(set.ena$points$Condition$HDSE)[,1]
# ena_second_points_d1 = as.matrix(set.ena$points$Condition$LDSE)[,1]
# ena_first_points_d2 = as.matrix(set.ena$points$Condition$HDSE)[,2] 
# ena_second_points_d2 = as.matrix(set.ena$points$Condition$LDSE)[,2]
# t_test_d1 = t.test(ena_first_points_d1, ena_second_points_d1)
# t_test_d2 = t.test(ena_first_points_d2, ena_second_points_d2)
# t_test_d1
# t_test_d2


# mean(ena_first_points_d1)
# mean(ena_second_points_d1)
# mean(ena_first_points_d2)
# mean(ena_second_points_d2)
# sd(ena_first_points_d1)
# sd(ena_second_points_d1)
# sd(ena_first_points_d2)
# sd(ena_second_points_d2)
# length(ena_first_points_d1)
# length(ena_second_points_d1)
# length(ena_first_points_d2)
# length(ena_second_points_d2)