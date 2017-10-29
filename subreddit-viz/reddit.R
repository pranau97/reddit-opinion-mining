source("Rstart.R")

library(sna)
library(ggnetwork)
library(svglite)
library(igraph)
library(intergraph)   # convert igraph to network
library(rsvg)   # convert svg to pdf

file_name <- "reddit-edge-list.csv"

df <- read_csv(file_name) %>% arrange(Source, Target)
#print(head(df))

defaults <- c("announcements","art","askreddit","askscience","aww","blog",
             "books","creepy","dataisbeautiful","diy","documentaries","earthporn",
             "explainlikeimfive","fitness","food","funny","futurology","gadgets",
             "gaming","getmotivated","gifs","history","iama","internetisbeautiful",
             "jokes","lifeprotips","listentothis","mildlyinteresting","movies","music",
             "news","nosleep","nottheonion","oldschoolcool","personalfinance",
             "philosophy","photoshopbattles","pics","science","showerthoughts",
             "space","sports","television","tifu","todayilearned","twoxchromosomes","upliftingnews",
             "videos","worldnews","writingprompts")

df <- df %>% mutate(connectDefault = ifelse(Source %in% defaults | Target %in% defaults, T, F))
#print(tail(df))

net <- graph.data.frame(df, directed=F)

#print(net)

V(net)$degree <- centralization.degree(net)$res
net <- igraph::delete.vertices(net, V(net)[degree < 3])

#print(net)

V(net)$group <- membership(cluster_walktrap(net, weights=E(net)$Weight))
V(net)$centrality <- eigen_centrality(net, weights=E(net)$Weight)$vector
V(net)$defaultnode <- V(net)$name %in% defaults

#print(head(data.frame(V(net)$name, V(net)$degree, V(net)$centrality, V(net)$group, V(net)$defaultnode)))

color_pool <- c(brewer.pal(9, "Blues")[6:9],
                brewer.pal(9, "Reds")[6:9],
                brewer.pal(9, "Greens")[6:9],
                brewer.pal(9, "Purples")[6:9])

n_colors <- max(V(net)$group)
set.seed(42)
palette <- data.frame(group=1:n_colors, colors=sample(color_pool, n_colors, replace=T), stringsAsFactors=FALSE)

V(net)$colornode <- palette[V(net)$group, 2]
                   
#print(head(palette))

df_edges <- tbl_df(data.frame(get.edgelist(net), stringsAsFactors=FALSE))
df_vertices <- tbl_df(data.frame(name=V(net)$name, color=V(net)$colornode, group=V(net)$group, stringsAsFactors=FALSE))

#print(head(df_edges))
#print(head(df_vertices))

default_edge_color <- "#cccccc"

df_edges <- df_edges %>% left_join(df_vertices, by=c("X1"="name")) %>% left_join(df_vertices, by=c("X2"="name"))
E(net)$coloredge <- ifelse(df_edges$group.x==df_edges$group.y, df_edges$color.x, default_edge_color)

#print(head(df_edges))

df_net <- ggnetwork(net, layout = "fruchtermanreingold", weights="Weight", niter=50000)

write.csv(df_net, "df_net.csv", row.names=F)
#print(head(df_net))

df_net_defaults = df_net[which(df_net$default),]
#print(head(df_net_defaults))

default_colors=c("#3498db", "#e67e22")
default_labels=c("Not Default", "Default")

svglite("subreddit-1.svg", width=10, height=8)  
  ggplot(df_net, aes(x = x, y = y, xend = xend, yend = yend, size = centrality)) +
    geom_edges(aes(color = connectDefault), size=0.05) +
    geom_nodes(aes(fill = defaultnode), shape = 21, stroke=0.2, color="black") +
    geom_nodelabel_repel(data=df_net, aes(color = defaultnode, label = vertex.names),
                          fontface = "bold", size=0.5, box.padding = unit(0.05, "lines"),
                          label.padding= unit(0.1, "lines"), segment.size=0.1, label.size=0.2) +
    scale_color_manual(values=default_colors, labels=default_labels, guide=F) +
    scale_fill_manual(values=default_colors, labels=default_labels) +
    ggtitle("Network Graph of Reddit Subreddits") +
    scale_size(range=c(0.1, 4)) + 
    theme_blank()
dev.off()

rsvg_pdf("subreddit-1.svg", "subreddit-1.pdf")

svglite("subreddit-2.svg", width=10, height=8)  
  ggplot(df_net, aes(x = x, y = y, xend = xend, yend = yend, size = centrality)) +
  geom_edges(aes(color = coloredge), size=0.05) +
  geom_nodes(aes(fill = colornode), shape = 21, stroke=0.2, color="black") +
     geom_nodelabel_repel(data=df_net, aes(color = colornode, label = vertex.names),
                       fontface = "bold", size=0.5,
                    box.padding = unit(0.05, "lines"), label.padding= unit(0.1, "lines"), segment.size=0.1, label.size=0.2) +
    scale_color_identity("colornode", guide=F) +
    scale_fill_identity("colornode", guide=F) +
    scale_size(range=c(0.2, 3), guide=F) +
    ggtitle("Network Graph of Reddit Subreddits") +
  theme_blank()
dev.off()

rsvg_pdf("subreddit-2.svg", "subreddit-2.pdf")

subreddit_graph_subset <- function(group_number) {

df_network <- df_net[which(df_net$group==group_number),]

plot <- 
  ggplot(df_network, aes(x = x, y = y, xend = xend, yend = yend, size = centrality)) +
  geom_edges(data=df_network[which(df_network$coloredge!=default_edge_color),], aes(color = coloredge), size=0.05) +
  geom_nodes(aes(fill = colornode), shape = 21, stroke=0.5, color="black") +
    geom_nodelabel_repel(data=df_network, aes(color = colornode, label = vertex.names),
                       fontface = "bold", family="Open Sans Condensed", size=1.5,
                    box.padding = unit(0.10, "lines"), label.padding= unit(0.1, "lines"), segment.size=0.1, label.size=0.5, label.r=unit(0.15, "lines")) +
    scale_color_identity("colornode", guide=F) +
    scale_fill_identity("colornode", guide=F) +
    scale_size(range=c(0.2, 6), guide=F) +
    ggtitle(sprintf("Network Subgraph of Group %s Subreddits",group_number)) +
  theme_blank(base_size=7, base_family="Source Sans Pro")
    
ggsave(sprintf("subreddit-groups/group-%03d.png", group_number), plot, width=4, height=3, dpi=300)

}

x <- lapply(1:max(V(net)$group), subreddit_graph_subset)
