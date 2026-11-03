/**
 * WeddingCraft — Google Sheets RSVP Backend
 *
 * SETUP:
 * 1. Create a new Google Sheet
 * 2. Go to Extensions → Apps Script
 * 3. Paste this entire file into Code.gs
 * 4. Click Deploy → New Deployment → Web App
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 5. Copy the Web App URL and paste it into config.json → rsvp.endpoint
 *
 * The script auto-creates headers on first submission.
 */

var SHEET_NAME = 'RSVP';

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName(SHEET_NAME);

    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
      sheet.appendRow([
        'Timestamp',
        'Guest Name',
        'Phone',
        'Guests Count',
        'Attending Events',
        'Dietary Preference',
        'Song Request',
        'Message',
        'Wedding'
      ]);
      sheet.getRange(1, 1, 1, 9).setFontWeight('bold');
      sheet.setFrozenRows(1);
    }

    sheet.appendRow([
      data.timestamp || new Date().toISOString(),
      data.name || '',
      data.phone || '',
      data.guests || '',
      data.events || '',
      data.diet || '',
      data.song || '',
      data.message || '',
      data.wedding || ''
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ status: 'ok', name: data.name }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({ status: 'ok', service: 'WeddingCraft RSVP' }))
    .setMimeType(ContentService.MimeType.JSON);
}
