from typing import IO, TypeVar

TextHTML = TypeVar("TextHTML", str, bytes, IO)
TextPlain = TypeVar("TextPlain", str, bytes, IO)
TextCss = TypeVar("TextCss", str, bytes, IO)
TextCsv = TypeVar("TextCsv", str, bytes, IO)
TextJavaScript = TypeVar("TextJavaScript", str, bytes, IO)
TextXml = TypeVar("TextXml", str, bytes, IO)

ApplicationJavaArchive = TypeVar("ApplicationJavaArchive", bytes, IO)
ApplicationEdiX12 = TypeVar("ApplicationEdiX12", str, bytes, IO)
ApplicationEdiFact = TypeVar("ApplicationEdiFact", str, bytes, IO)
ApplicationJavaScript = TypeVar("ApplicationJavaScript", str, bytes, IO)
ApplicationOctetStream = TypeVar("ApplicationOctetStream", str, bytes, IO)
ApplicationOgg = TypeVar("ApplicationOgg", bytes, IO)
ApplicationPdf = TypeVar("ApplicationPdf", bytes, IO)
ApplicationXHtmlXml = TypeVar("ApplicationXHtmlXml", str, bytes, IO)
ApplicationXShockwaveFlash = TypeVar("ApplicationXShockwaveFlash", bytes, IO)
ApplicationJson = TypeVar("ApplicationJson", str, bytes, dict, list, IO)
ApplicationLdJson = TypeVar("ApplicationLdJson", str, bytes, IO)
ApplicationXml = TypeVar("ApplicationXml", str, bytes, IO)
ApplicationZip = TypeVar("ApplicationZip", bytes, IO)
ApplicationXWWWFormUrlEncoded = TypeVar("ApplicationXWWWFormUrlEncoded", str, bytes, IO)

ApplicationVndAndroidPackageArchive = TypeVar(
    "ApplicationVndAndroidPackageArchive", bytes, IO
)
ApplicationVndOasisOpenDocumentText = TypeVar(
    "ApplicationVndOasisOpenDocumentText", bytes, IO
)
ApplicationVndOasisOpenDocumentSpreadsheet = TypeVar(
    "ApplicationVndOasisOpenDocumentSpreadsheet", bytes, IO
)
ApplicationVndOasisOpenDocumentPresentation = TypeVar(
    "ApplicationVndOasisOpenDocumentPresentation", bytes, IO
)
ApplicationVndOasisOpenDocumentGraphics = TypeVar(
    "ApplicationVndOasisOpenDocumentGraphics", bytes, IO
)
ApplicationVndMsExcel = TypeVar("ApplicationVndMsExcel", bytes, IO)
ApplicationVndOpenXmlFormatsOfficeDocumentSpreadsheetmlSheet = TypeVar(
    "ApplicationVndOpenXmlFormatsOfficeDocumentSpreadsheetmlSheet", bytes, IO
)
ApplicationVndMsPowerpoint = TypeVar("ApplicationVndMsPowerpoint", bytes, IO)
ApplicationVndOpenXmlFormatsOfficeDocumentPresentationmlPresentation = TypeVar(
    "ApplicationVndOpenXmlFormatsOfficeDocumentPresentationmlPresentation", bytes, IO,
)
ApplicationMsWord = TypeVar("ApplicationMsWord", bytes, IO,)
ApplicationVndOpenXmlFormatsOfficeDocumentWordProcessingmlDocument = TypeVar(
    "ApplicationVndOpenXmlFormatsOfficeDocumentWordProcessingmlDocument", bytes, IO,
)
ApplicationVndMozillaXulXml = TypeVar("ApplicationVndMozillaXulXml", bytes, IO,)

AudioMpeg = TypeVar("AudioMpeg", bytes, IO)
AudioXMsWma = TypeVar("AudioXMsWma", bytes, IO)
AudioVndRnRealAudio = TypeVar("AudioVndRnRealAudio", bytes, IO)
AudioXWav = TypeVar("AudioXWav", bytes, IO)

ImageGif = TypeVar("ImageGif", bytes, IO)
ImageJpeg = TypeVar("ImageJpeg", bytes, IO)
ImagePng = TypeVar("ImagePng", bytes, IO)
ImageTiff = TypeVar("ImageTiff", bytes, IO)
ImageVndMicrosoftIcon = TypeVar("ImageVndMicrosoftIcon", bytes, IO)
ImageXIcon = TypeVar("ImageXIcon", bytes, IO)
ImageVndDjvu = TypeVar("ImageVndDjvu", bytes, IO)
ImageSvgXml = TypeVar("ImageSvgXml", bytes, IO)

MultipartMixed = TypeVar("MultipartMixed", str, bytes, IO)
MultipartAlternative = TypeVar("MultipartAlternative", str, bytes, IO)
MultipartRelated = TypeVar("MultipartRelated", str, bytes, IO)
MultipartFormData = TypeVar("MultipartFormData", str, bytes, IO)

VideoMpeg = TypeVar("VideoMpeg", bytes, IO)
VideoMp4 = TypeVar("VideoMp4", bytes, IO)
VideoQuicktime = TypeVar("VideoQuicktime", bytes, IO)
VideoXMsWmv = TypeVar("VideoXMsWmv", bytes, IO)
VideoXMsVideo = TypeVar("VideoXMsVideo", bytes, IO)
VideoXFlv = TypeVar("VideoXFlv", bytes, IO)
VideoWebm = TypeVar("VideoWebm", bytes, IO)

ContentTypes = [
    TextHTML,
    TextPlain,
    TextCss,
    TextCsv,
    TextJavaScript,
    TextXml,
    ApplicationJavaArchive,
    ApplicationEdiX12,
    ApplicationEdiFact,
    ApplicationJavaScript,
    ApplicationOctetStream,
    ApplicationOgg,
    ApplicationPdf,
    ApplicationXHtmlXml,
    ApplicationXShockwaveFlash,
    ApplicationJson,
    ApplicationLdJson,
    ApplicationXml,
    ApplicationZip,
    ApplicationXWWWFormUrlEncoded,
    AudioMpeg,
    AudioXMsWma,
    AudioVndRnRealAudio,
    AudioXWav,
    ImageGif,
    ImageJpeg,
    ImagePng,
    ImageTiff,
    ImageVndMicrosoftIcon,
    ImageXIcon,
    ImageVndDjvu,
    ImageSvgXml,
    MultipartMixed,
    MultipartAlternative,
    MultipartRelated,
    MultipartFormData,
    VideoMpeg,
    VideoMp4,
    VideoQuicktime,
    VideoXMsWmv,
    VideoXMsVideo,
    VideoXFlv,
    VideoWebm,
    ApplicationVndAndroidPackageArchive,
    ApplicationVndOasisOpenDocumentText,
    ApplicationVndOasisOpenDocumentSpreadsheet,
    ApplicationVndOasisOpenDocumentPresentation,
    ApplicationVndOasisOpenDocumentGraphics,
    ApplicationVndMsExcel,
    ApplicationVndOpenXmlFormatsOfficeDocumentSpreadsheetmlSheet,
    ApplicationVndMsPowerpoint,
    ApplicationVndOpenXmlFormatsOfficeDocumentPresentationmlPresentation,
    ApplicationMsWord,
    ApplicationVndOpenXmlFormatsOfficeDocumentWordProcessingmlDocument,
    ApplicationVndMozillaXulXml,
]

CONTENT_TYPE_MAP = {
    TextHTML: "text/html",
    TextPlain: "text/plain",
    TextCss: "text/css",
    TextCsv: "text/csv",
    TextJavaScript: "text/javascript",
    TextXml: "text/xml",
    ApplicationJavaArchive: "application/java-archive",
    ApplicationEdiX12: "application/EDI-X12",
    ApplicationEdiFact: "application/EDIFACT",
    ApplicationJavaScript: "application/javascript",
    ApplicationOctetStream: "application/octet-stream",
    ApplicationOgg: "application/ogg",
    ApplicationPdf: "application/pdf",
    ApplicationXHtmlXml: "application/xhtml+xml",
    ApplicationXShockwaveFlash: "application/x-shockwave-flash",
    ApplicationJson: "application/json",
    ApplicationLdJson: "application/ld+json",
    ApplicationXml: "application/xml",
    ApplicationZip: "application/zip",
    ApplicationXWWWFormUrlEncoded: "application/x-www-form-urlencoded",
    AudioMpeg: "audio/mpeg",
    AudioXMsWma: "audio/x-ms-wma",
    AudioVndRnRealAudio: "audio/vnd.rn-realaudio",
    AudioXWav: "audio/x-wav",
    ImageGif: "image/gif",
    ImageJpeg: "image/jpeg",
    ImagePng: "image/png",
    ImageTiff: "image/tiff",
    ImageVndMicrosoftIcon: "image/vnd.microsoft.icon",
    ImageXIcon: "image/x-icon",
    ImageVndDjvu: "image/vnd.djvu",
    ImageSvgXml: "image/svg+xml",
    MultipartMixed: "multipart/mixed",
    MultipartAlternative: "multipart/alternative",
    MultipartRelated: "multipart/related",
    MultipartFormData: "multipart/form-data",
    VideoMpeg: "video/mpeg",
    VideoMp4: "video/mp4",
    VideoQuicktime: "video/quicktime",
    VideoXMsWmv: "video/x-ms-wmv",
    VideoXMsVideo: "video/x-msvideo",
    VideoXFlv: "video/x-flv",
    VideoWebm: "video/webm",
    ApplicationVndAndroidPackageArchive: "application/vnd.android.package-archive",
    ApplicationVndOasisOpenDocumentText: "application/vnd.oasis.opendocument.text",
    ApplicationVndOasisOpenDocumentSpreadsheet: "application/vnd.oasis.opendocument."
    "spreadsheet",
    ApplicationVndOasisOpenDocumentPresentation: "application/vnd.oasis.opendocument."
    "presentation",
    ApplicationVndOasisOpenDocumentGraphics: "application/vnd.oasis.opendocument."
    "graphics",
    ApplicationVndMsExcel: "application/vnd.ms-excel",
    ApplicationVndOpenXmlFormatsOfficeDocumentSpreadsheetmlSheet: "application/vnd."
    "openxmlformats-officedocument.spreadsheetml.sheet",
    ApplicationVndMsPowerpoint: "application/vnd.ms-powerpoint",
    ApplicationVndOpenXmlFormatsOfficeDocumentPresentationmlPresentation: "application/"
    "vnd.openxmlformats-officedocument.presentationml.presentation",
    ApplicationMsWord: "application/msword",
    ApplicationVndOpenXmlFormatsOfficeDocumentWordProcessingmlDocument: "application/"
    "vnd.openxmlformats-officedocument.wordprocessingml.document",
    ApplicationVndMozillaXulXml: "application/vnd.mozilla.xul+xml",
}
