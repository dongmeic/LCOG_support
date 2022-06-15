# Objective: to prepare spatial data for the bike share trip ends during May 2018 and May 2022
# By Dongmei Chen (dchen@lcog.org)
# On June 3rd, 2022
library(rgdal)
source("T:/DCProjects/GitHub/common_functions.R")

path <- "T:/DCProjects/StoryMap/BikeCounting/BikeShare/Data/Output/review"

selected_vars <- c('User.ID', 'Route.ID', 'Start.Hub', 
                   'Start.Latitude', 'Start.Longitude',
                   'Start.Date', 'Start.Time', 
                   'End.Hub', 'End.Latitude', 'End.Longitude',
                   'End.Date', 'End.Time', 'Bike.ID', 'Bike.Name',
                   'Distance..Miles.', 'Duration')

df <- cbdf(path, vars="selected", selected_vars=selected_vars)
# startlon <- -123.05014
# endlon <- -122.87815
# startlat <- 44.00676
# endlat <- 44.10293
# 
# # Springfield data
# sdf <- df[(df$Start.Latitude >= startlat & df$Start.Latitude <= endlat) & 
#             (df$Start.Longitude >= startlon & df$Start.Longitude <= endlon) & 
#             (df$End.Latitude >= startlat & df$End.Latitude <= endlat) &
#             (df$End.Longitude >= startlon & df$End.Longitude <= endlon), ]

#sdf <- sdf[!(sdf$Start.Longitude == sdf$End.Longitude & sdf$Start.Latitude == sdf$End.Latitude),]

sdf <- df
#start_hb <- unique(sdf[,c("Start.Hub","Start.Latitude","Start.Longitude")])
end_hb <- sdf[,c("End.Hub","End.Latitude","End.Longitude")]

#colnames(start_hb) <- c("Name", "Latitude", "Longitude")
colnames(end_hb) <- c("Name", "Latitude", "Longitude")
sum_end_df <- aggregate(x=list(count=end_hb$Name), 
                        by=list(name=end_hb$Name,
                                lon=end_hb$Longitude, 
                                lat=end_hb$Latitude),
                        FUN=function(x) length(x))
locspdf <- df2spdf(sum_end_df, 'lon', 'lat')
outpath <- "T:/DCProjects/StoryMap/BikeCounting/BikeShare/Output"
writeOGR(locspdf, dsn=outpath, layer="bike_share_loc_end_all", driver="ESRI Shapefile", overwrite_layer=TRUE)

#start_hb$OrgDest <- rep("Origin", dim(start_hb)[1])
#end_hb$OrgDest <- rep("Destination", dim(end_hb)[1])
stations <- read.csv("T:/DCProjects/GitHub/BikeCounting/BikeMap/BikeShareStations.csv")
spr_hubs <- c("Heartfelt House", "RiverBend Annex", "PeaceHealth RiverBend")
for(name in spr_hubs){
  end_hb[end_hb$Name==name, "Latitude"] <- stations[stations$name==name, "lat"]
  end_hb[end_hb$Name==name, "Longitude"] <- stations[stations$name==name, "lon"]
}

agg_end <- data.frame(table(end_hb[!(end_hb$Name %in% spr_hubs), "Name"]))
colnames(agg_end) <- c("name", "count")
agg_lonlat <- aggregate(x=list(lon=end_hb$Longitude, 
                            lat=end_hb$Latitude), 
                        by=list(name=end_hb$Name),
                        FUN=mean)
locdf <- merge(agg_end, agg_lonlat, by="name")
#locdf <- rbind(start_hb, end_hb)
#locdf <- end_hb[na.omit(end_hb$Latitude) & na.omit(end_hb$Longitude),]

locspdf <- df2spdf(locdf, 'lon', 'lat')
ugb <- readOGR(dsn = "T:/DCProjects/StoryMap/BikeCounting/BikeCounts/ReviewBikeCounts/ReviewBikeCounts.gdb",
               layer = "CLMPO_UGB")
ugb <- spTransform(ugb, CRS(proj4string(MPOBound)))
#spr <- ugb[ugb$ugbcity == 'SPR',]
# inside.polygon <- over(locspdf, ugb[,"ugbcity"])
# locspdf$ugbcity <- inside.polygon$ugbcity
# 
# spr_df <- locspdf@data[locspdf@data$ugbcity == "SPR",]
# spr_spdf <- df2spdf(spr_df, 'Longitude', 'Latitude') # something wrong in the "over" or "filter" steps
  
#writeOGR(locspdf, dsn=outpath, layer="bike_share_loc_spr", driver="ESRI Shapefile", overwrite_layer=TRUE)
writeOGR(locspdf, dsn=outpath, layer="bike_share_loc_end", driver="ESRI Shapefile", overwrite_layer=TRUE)

# end_hb has been edited here
sum_end_df <- aggregate(x=list(count=end_hb$Name), 
                        by=list(name=end_hb$Name,
                                lon=end_hb$Longitude, 
                                lat=end_hb$Latitude),
                        FUN=function(x) length(x))
locspdf <- df2spdf(sum_end_df, 'lon', 'lat')
writeOGR(locspdf, dsn=outpath, layer="bike_share_loc_end_detail", driver="ESRI Shapefile", overwrite_layer=TRUE)

# after "select by location"
trip_end_002 <- readOGR(dsn = "T:/DCProjects/Support/PHR/Trip_End_Locs_002", layer = "Trip_End_Locs_002")
grep("Hilyard", stations$name, value = TRUE)
#"17th & Hilyard"
