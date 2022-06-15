library(leaflet.extras)
library(rgdal)
library(tidyverse)
library(ggmap)
library(stringr)
library(viridis)
library(rjson)

trip_end <- readOGR(dsn = "T:/DCProjects/Support/PHR", layer="trip_end_locs_002miles")
trip_holds <- readOGR(dsn = "T:/DCProjects/Support/PHR", layer="trip_holds_002miles")

api_key <- fromJSON(file = "T:/DCProjects/GitHub/BikeCounting/config/keys.json")$google_maps$APIKEY2
register_google(key = api_key)
map_sf <- get_map('Eugene', zoom = 12, maptype = 'roadmap')

ggmap(map_sf) +
  stat_density2d(data = trip_end@data, aes(x = lon, y = lat, fill = ..density..), geom = 'tile', contour = F, alpha = .5) +
  scale_fill_viridis(option = 'inferno') +
  labs(title = str_c('Bike share trip end locations in Eugene'
  )
  ,subtitle = '  '
  ,fill = str_c('')
  ) +
  theme(text = element_text(color = "#444444")
        ,plot.title = element_text(size = 22, face = 'bold')
        ,plot.subtitle = element_text(size = 12)
        ,axis.text = element_blank()
        ,axis.title = element_blank()
        ,axis.ticks = element_blank()
  ) +
  guides(fill = guide_legend(override.aes= list(alpha = 1)))

ggmap(map_sf) +
  stat_density2d(data = trip_end@data, aes(x = lon, y = lat, fill = ..density..), geom = 'tile', contour = F, alpha = .5) +
  scale_fill_viridis(option = 'inferno') +
  labs(title = str_c('Bike share trip end in Eugene'
  )
  ,subtitle = '  '
  ,fill = str_c('')
  ) +
  theme(text = element_text(color = "#444444")
        ,plot.title = element_text(size = 22, face = 'bold')
        ,plot.subtitle = element_text(size = 12)
        ,axis.text = element_blank()
        ,axis.title = element_blank()
        ,axis.ticks = element_blank()
  ) +
  guides(fill = guide_legend(override.aes= list(alpha = 1)))

leaflet() %>% 
addProviderTiles(provider = providers$OpenTopoMap) %>% 
addWebGLHeatmap(data = trip_end, size = 2500, units = "m", intensity = 0.5)