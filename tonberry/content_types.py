from typing import IO, Type, TypeVar

from tonberry.util import File

TextHTML = TypeVar("TextHTML", str, bytes, IO, File)
TextPlain = TypeVar("TextPlain", str, bytes, IO, File)
TextCss = TypeVar("TextCss", str, bytes, IO, File)
TextCsv = TypeVar("TextCsv", str, bytes, IO, File)
TextJavaScript = TypeVar("TextJavaScript", str, bytes, IO, File)
TextXml = TypeVar("TextXml", str, bytes, IO, File)

ApplicationJavaArchive = TypeVar("ApplicationJavaArchive", bytes, IO, File)
ApplicationEdiX12 = TypeVar("ApplicationEdiX12", str, bytes, IO, File)
ApplicationEdiFact = TypeVar("ApplicationEdiFact", str, bytes, IO, File)
ApplicationJavaScript = TypeVar("ApplicationJavaScript", str, bytes, IO, File)
ApplicationOctetStream = TypeVar("ApplicationOctetStream", str, bytes, IO, File)
ApplicationOgg = TypeVar("ApplicationOgg", bytes, IO, File)
ApplicationPdf = TypeVar("ApplicationPdf", bytes, IO, File)
ApplicationXHtmlXml = TypeVar("ApplicationXHtmlXml", str, bytes, IO, File)
ApplicationXShockwaveFlash = TypeVar("ApplicationXShockwaveFlash", bytes, IO, File)
ApplicationJson = TypeVar(
    "ApplicationJson",
    str,
    bytes,
    dict,
    list,
    int,
    str,
    float,
    bool,
    Type[None],
    IO,
    File,
)
ApplicationLdJson = TypeVar("ApplicationLdJson", str, bytes, IO, File)
ApplicationXml = TypeVar("ApplicationXml", str, bytes, IO, File)
ApplicationZip = TypeVar("ApplicationZip", bytes, IO, File)
ApplicationXWWWFormUrlEncoded = TypeVar(
    "ApplicationXWWWFormUrlEncoded", str, bytes, IO, File
)

ApplicationVndAndroidPackageArchive = TypeVar(
    "ApplicationVndAndroidPackageArchive", bytes, IO, File
)
ApplicationVndOasisOpenDocumentText = TypeVar(
    "ApplicationVndOasisOpenDocumentText", bytes, IO, File
)
ApplicationVndOasisOpenDocumentSpreadsheet = TypeVar(
    "ApplicationVndOasisOpenDocumentSpreadsheet", bytes, IO, File
)
ApplicationVndOasisOpenDocumentPresentation = TypeVar(
    "ApplicationVndOasisOpenDocumentPresentation", bytes, IO, File
)
ApplicationVndOasisOpenDocumentGraphics = TypeVar(
    "ApplicationVndOasisOpenDocumentGraphics", bytes, IO, File
)
ApplicationVndMsExcel = TypeVar("ApplicationVndMsExcel", bytes, IO, File)
ApplicationVndOpenXmlFormatsOfficeDocumentSpreadsheetmlSheet = TypeVar(
    "ApplicationVndOpenXmlFormatsOfficeDocumentSpreadsheetmlSheet", bytes, IO, File
)
ApplicationVndMsPowerpoint = TypeVar("ApplicationVndMsPowerpoint", bytes, IO, File)
ApplicationVndOpenXmlFormatsOfficeDocumentPresentationmlPresentation = TypeVar(
    "ApplicationVndOpenXmlFormatsOfficeDocumentPresentationmlPresentation",
    bytes,
    IO,
    File,
)
ApplicationMsWord = TypeVar(
    "ApplicationMsWord",
    bytes,
    IO,
)
ApplicationVndOpenXmlFormatsOfficeDocumentWordProcessingmlDocument = TypeVar(
    "ApplicationVndOpenXmlFormatsOfficeDocumentWordProcessingmlDocument",
    bytes,
    IO,
    File,
)
ApplicationVndMozillaXulXml = TypeVar("ApplicationVndMozillaXulXml", bytes, IO, File)

AudioMpeg = TypeVar("AudioMpeg", bytes, IO, File)
AudioXMsWma = TypeVar("AudioXMsWma", bytes, IO, File)
AudioVndRnRealAudio = TypeVar("AudioVndRnRealAudio", bytes, IO, File)
AudioXWav = TypeVar("AudioXWav", bytes, IO, File)

ImageGif = TypeVar("ImageGif", bytes, IO, File)
ImageJpeg = TypeVar("ImageJpeg", bytes, IO, File)
ImagePng = TypeVar("ImagePng", bytes, IO, File)
ImageTiff = TypeVar("ImageTiff", bytes, IO, File)
ImageVndMicrosoftIcon = TypeVar("ImageVndMicrosoftIcon", bytes, IO, File)
ImageXIcon = TypeVar("ImageXIcon", bytes, IO, File)
ImageVndDjvu = TypeVar("ImageVndDjvu", bytes, IO, File)
ImageSvgXml = TypeVar("ImageSvgXml", bytes, IO, File)

MultipartMixed = TypeVar("MultipartMixed", str, bytes, IO, File)
MultipartAlternative = TypeVar("MultipartAlternative", str, bytes, IO, File)
MultipartRelated = TypeVar("MultipartRelated", str, bytes, IO, File)
MultipartFormData = TypeVar("MultipartFormData", str, bytes, IO, File)

VideoMpeg = TypeVar("VideoMpeg", bytes, IO, File)
VideoMp4 = TypeVar("VideoMp4", bytes, IO, File)
VideoQuicktime = TypeVar("VideoQuicktime", bytes, IO, File)
VideoXMsWmv = TypeVar("VideoXMsWmv", bytes, IO, File)
VideoXMsVideo = TypeVar("VideoXMsVideo", bytes, IO, File)
VideoXFlv = TypeVar("VideoXFlv", bytes, IO, File)
VideoWebm = TypeVar("VideoWebm", bytes, IO, File)

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
