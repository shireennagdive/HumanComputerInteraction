# Title     : Statistical tests
# Objective : TODO
# Created by: shireennagdive,mohitchoudhary
# Created on: 11/6/18
library("ggpubr")
library("gplots")
#DATASET 1
df_between_subjects <- read.csv("/Users/shireennagdive/Semester1/HumanComputerInteraction/Assignments/Assignment2/group8_dataset1.csv",
               header = T)

#anova
fit <- aov(time ~ menu, data=df_between_subjects)
print(summary(fit))

#boxplot
ggboxplot(df_between_subjects,
x = "menu", y = "time", color = "group", palette = c("#00AFBB", "#E7B800", "#FC4E07"), order = c("controlmenu", "flowmenu", "toolglass",  "toolpalette"), ylab = "Menu", xlab = "Time")

#mean plot
plotmeans(time ~ menu, data = df_between_subjects, frame = FALSE,
xlab = "Menus", ylab = "Time",
main="Mean Plot with 95% CI")
ggline(df_between_subjects, x = "menu", y = "time",
add = c("mean_se", "jitter"),
order = c("ctrl", "trt1", "trt2"),
ylab = "Time", xlab = "Menu")

#Residuals Plot
plot(fit, 1)
#Normality Plot
plot(fit, 2)

#t test
print(pairwise.t.test(df_between_subjects$time,df_between_subjects$menu,p.adj = "bonferroni"))

#DATASET2

df_within_subjects <- read.csv("/Users/shireennagdive/Semester1/HumanComputerInteraction/Assignments/Assignment2/group8_dataset2.csv", header = T)

#manova
mav.stat <- manova(cbind(time, error) ~ menu + Error(user/(menu)), data=df_within_subjects)
print(summary(mav.stat,tol=0))


#boxplot
ggboxplot(df_within_subjects,
x = "menu", y = "time", color = "group", palette = c("#00AFBB", "#E7B800", "#FC4E07"), order = c("controlmenu", "flowmenu", "toolglass",  "toolpalette"), ylab = "Menu", xlab = "Time")

#boxplot
ggboxplot(df_within_subjects,
x = "menu", y = "error", color = "group", palette = c("#00AFBB", "#E7B800", "#FC4E07"), order = c("controlmenu", "flowmenu", "toolglass",  "toolpalette"), ylab = "Menu", xlab = "Error")

#t test
pairwise.t.test(df_within_subjects$time,df_within_subjects$menu,p.adj = "bonferroni",paired=TRUE)
pairwise.t.test(df_within_subjects$error,df_within_subjects$menu,p.adj = "bonferroni",paired=TRUE)
