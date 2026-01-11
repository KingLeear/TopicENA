required_packages <- c(
  "rENA"
)

installed <- rownames(installed.packages())

for (pkg in required_packages) {
  if (!pkg %in% installed) {
    message(paste("Installing R package:", pkg))
    install.packages(pkg, repos = "https://cloud.r-project.org")
  }
}

message("All required R packages are installed.")
