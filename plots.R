d <- read.csv("~/Desktop/Deliveries//profits2.csv")
d <- na.omit(d)
head(d)
attach(d)

library(ggplot2)
ggplot(d, aes(x=Revenue)) + 
	geom_histogram(colour="black", fill="lightblue") +
	labs(x="Revenue", y="Count")

ggplot(d, aes(x=Revenue)) + 
	geom_histogram(aes(y=..density..), colour="black", fill="grey", binwidth=20000) +
	labs(x="Revenue", y="Density") + geom_density(alpha=.2, fill="pink")

ggplot(d, aes(x=Cost)) + 
	geom_histogram(colour="black", fill="lightblue") +
	labs(x="Cost", y="Count")

ggplot(d, aes(x=Cost)) + 
	geom_histogram(aes(y=..density..), colour="black", fill="grey", binwidth=50) +
	labs(x="Cost", y="Density") + geom_density(alpha=.2, fill="pink")

ggplot(d, aes(x=Profit)) + 
	geom_histogram(colour="black", fill="lightblue") +
	labs(x="Profit", y="Count")

ggplot(d, aes(x=Profit)) + 
	geom_histogram(aes(y=..density..), colour="black", fill="grey", binwidth=20000) +
	labs(x="Profit", y="Density") + geom_density(alpha=.2, fill="pink")

line <- predict(lm(Revenue ~ Cost, data = d))
ggplot(d, aes(y = Revenue, x = Cost)) +
	geom_point(aes(color = Profit)) +
	geom_line(aes(y = line))
