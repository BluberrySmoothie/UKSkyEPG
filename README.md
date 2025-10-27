## Support the Project
If you like my work, feel free to buy me a coffee! ☕
https://buymeacoffee.com/BluberrySmoothie


# UKSkyEPG
Python code to extract Sky UK's EPG data from their publicly accessible API

This Python code will query the Sky UK API to obtain 8 days of TV guide and output as an XMLTV format.

It requires a csv file named "SkyChannels.csv" This should contain the "SID" for Skys API and the TVG-ID you want on the output guide. For Example:

1001,SDSkyAction
1003,HDMUTV
1009,QTVReligious
1011,PBC
1016,ZeeTVHD
1017,ThatsTV
1018,Cruise1st.tv.
1019,CNNHD
1022,HDSkyintro

NOTE: The SID is not the same as the channel number. To find the SID you can use this website:
https://www.satellite-calculations.com/DVB/28.2E/bskyb.php?4110/0
The SID is listed as "Channel ID"


I can't say this is 100% working. Its my 1st attempt..
