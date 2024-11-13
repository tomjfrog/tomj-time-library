package com.tomfjrog.time;



import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
// Supplied by the Guava dependency
import com.google.common.base.Joiner;

public class TimeUtils {

    // Function to return current system time
    public static String getCurrentSystemTime() {
        ZonedDateTime currentTime = ZonedDateTime.now();
        return currentTime.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss z"));
    }

    public static String reportSupportedZones() {
        System.out.println("I support TZDB 2005r timezones such as the following:");
        Joiner joiner = Joiner.on("; ").skipNulls();
        return joiner.join("CST", null, "MST", "EST");
    }

    // Function to return the current system time in a given time zone
    public static String getCurrentTimeInTimeZone(String timeZone) {
        try {
            ZoneId zoneId = ZoneId.of(timeZone);
            ZonedDateTime currentTimeInZone = ZonedDateTime.now(zoneId);
            return currentTimeInZone.format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss z"));
        } catch (Exception e) {
            return "Invalid time zone: " + timeZone;
        }
    }
}
