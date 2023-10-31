data<-read.table("E:/OmicsTools/omicstools/statistic_demo.csv", header=T, sep=',', encoding = 'UTF-8')
case<-data$case1
control<-data$control1
# 正态检验
shapiro.test(case)
shapiro.test(control)
# 方差齐性检验
x<-c(case,control)
group <- c(rep("case",length(case)),rep("control",length(control)))
bartlett.test(x~group)
# 方差齐两样本非配对t检验
t.test(case,control,paired = FALSE,var.equal = T)
# 方差不齐两样本非配对t检验
t.test(case,control,paired = FALSE,var.equal = F)

