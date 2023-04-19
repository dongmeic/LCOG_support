
path <- 'T:/DCProjects/Support/Lane/HfG'
am <- read.csv(paste0(path,'/output/application_members.csv'))
lane_cities <- c('Eugene', 'Springfield', 'Coburg', 'Creswell', 'Cottage Grove', 'Dunes City', 
  'Florence', 'Junction City', 'Lowell', 'Oakridge', 'Veneta', 'Westfir')

length(unique(am[am$LegalCity %in% lane_cities, "ID"]))/length(unique(am$ID))
colnames(am)
length(unique(am[am$AgeNotes %in% c("Children (3-12)","Infants (0-2)", "Teenagers (13-17)"), "ID"]))/length(unique(am$ID))
length(unique(am[am$Race2 != "White", "ID"]))/length(unique(am$ID))
unique(am$Race2)
unique(am$EthniNotes)
length(unique(am[am$EthniNotes == "Hispanic or Latino", "ID"]))/length(unique(am$ID))

oa <- read.csv(paste0(path,'/output/online_application.csv'))
colnames(oa)
length(unique(oa[oa$Poverty == "Below poverty level", "ID"]))/length(unique(oa$ID))

aqh <- read.csv(paste0(path,'/output/question_history.csv'))
colnames(aqh)
unique(aqh[,c("Question","Preference" )])
unique(aqh[aqh$Preference == 'P9', 'Response'])


