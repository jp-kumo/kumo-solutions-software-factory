import React, { useEffect, useMemo, useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, Youtube, Loader2, CheckCircle, FileType, MonitorPlay } from 'lucide-react';

function App() {
  const [url, setUrl] = useState('');
  const [videoInfo, setVideoInfo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [message, setMessage] = useState(null);
  const [settings, setSettings] = useState({
    quality_profiles: ['balanced'],
    transcript_formats: ['txt', 'md', 'pdf'],
    default_quality_profile: 'balanced',
  });
  const [qualityProfile, setQualityProfile] = useState('balanced');

  const transcriptFormats = useMemo(() => settings?.transcript_formats || ['txt', 'md', 'pdf'], [settings]);

  const getErrorText = (err, fallback) => {
    return err?.response?.data?.detail || fallback;
  };

  useEffect(() => {
    const loadSettings = async () => {
      try {
        const res = await axios.get('/api/settings');
        setSettings(res.data);
        setQualityProfile(res.data.default_quality_profile || 'balanced');
      } catch {
        // Keep default settings in offline/dev fallback mode.
      }
    };

    loadSettings();
  }, []);

  const fetchInfo = async () => {
    if (!url) return;
    setLoading(true);
    setMessage(null);
    setVideoInfo(null);
    try {
      const res = await axios.post('/api/info', { url });
      setVideoInfo(res.data);
    } catch (err) {
      setMessage({ type: 'error', text: getErrorText(err, 'Failed to fetch video info. Check URL.') });
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadVideo = async () => {
    if (!url) return;
    setDownloading(true);
    try {
      await axios.post('/api/download', { url, quality_profile: qualityProfile });
      setMessage({ type: 'success', text: `Video downloaded (${qualityProfile}) to your Downloads folder.` });
    } catch (err) {
      setMessage({ type: 'error', text: getErrorText(err, 'Failed to download video.') });
    } finally {
      setDownloading(false);
    }
  };

  const handleDownloadTranscript = async (fmt) => {
    if (!videoInfo) return;
    setDownloading(true);
    try {
      await axios.post('/api/transcript', {
        url,
        video_id: videoInfo.id,
        title: videoInfo.title,
        fmt,
      });
      setMessage({ type: 'success', text: `Transcript (${fmt.toUpperCase()}) saved to your Downloads folder.` });
    } catch (err) {
      setMessage({ type: 'error', text: getErrorText(err, 'Failed to download transcript. Captions might be missing.') });
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 font-sans selection:bg-red-500 selection:text-white">
      <div className="max-w-4xl mx-auto px-6 py-12">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="flex justify-center mb-4">
            <div className="p-4 bg-red-600/20 rounded-full">
              <Youtube className="w-12 h-12 text-red-500" />
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-red-500 to-orange-500 mb-4">
            YT Downloader Pro
          </h1>
          <p className="text-gray-400 text-lg">Download videos & convert transcripts with premium ease.</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="relative group mb-12"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-red-600 to-orange-600 rounded-xl blur opacity-25 group-hover:opacity-50 transition duration-500"></div>
          <div className="relative flex bg-gray-800 rounded-xl p-2 border border-gray-700 shadow-2xl">
            <input
              type="text"
              placeholder="Paste YouTube URL here..."
              className="w-full bg-transparent border-none outline-none text-white px-4 text-lg placeholder-gray-500"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && fetchInfo()}
            />
            <button
              onClick={fetchInfo}
              disabled={loading}
              className="bg-red-600 hover:bg-red-500 text-white px-8 py-3 rounded-lg font-medium transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <MonitorPlay className="w-5 h-5" />}
              Fetch
            </button>
          </div>
        </motion.div>

        <AnimatePresence>
          {videoInfo && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl overflow-hidden shadow-2xl"
            >
              <div className="grid md:grid-cols-2 gap-0">
                <div className="relative group">
                  <img src={videoInfo.thumbnail} alt="Thumbnail" className="w-full h-full object-cover min-h-[250px]" />
                  <div className="absolute inset-0 bg-black/40 group-hover:bg-black/20 transition-all duration-300"></div>
                </div>

                <div className="p-8 flex flex-col justify-center">
                  <h2 className="text-2xl font-bold mb-2 line-clamp-2">{videoInfo.title}</h2>
                  <p className="text-gray-400 mb-2 flex items-center gap-2">
                    <span className="px-2 py-1 bg-gray-700 rounded text-xs font-mono">HD</span>
                    <span>Video ID: {videoInfo.id}</span>
                  </p>

                  <label className="block text-sm text-gray-300 mb-6">
                    <span className="mr-2">Quality profile:</span>
                    <select
                      className="bg-gray-900 border border-gray-600 rounded-md px-3 py-1.5 text-gray-100"
                      value={qualityProfile}
                      onChange={(e) => setQualityProfile(e.target.value)}
                      disabled={downloading}
                    >
                      {settings.quality_profiles.map((profile) => (
                        <option key={profile} value={profile}>
                          {profile}
                        </option>
                      ))}
                    </select>
                  </label>

                  <div className="space-y-4">
                    <button
                      onClick={handleDownloadVideo}
                      disabled={downloading}
                      className="w-full bg-white text-gray-900 hover:bg-gray-100 px-6 py-4 rounded-xl font-bold transition-all flex items-center justify-center gap-3 disabled:opacity-50"
                    >
                      {downloading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Download className="w-5 h-5" />}
                      Download Video (MP4)
                    </button>

                    <div className="grid grid-cols-3 gap-2">
                      {transcriptFormats.map((fmt) => (
                        <button
                          key={fmt}
                          onClick={() => handleDownloadTranscript(fmt)}
                          disabled={downloading}
                          className="bg-gray-700 hover:bg-gray-600 text-gray-200 py-3 rounded-lg font-medium transition-all flex flex-col items-center justify-center gap-1 text-sm border border-gray-600 hover:border-gray-500 disabled:opacity-50"
                        >
                          <FileType className="w-4 h-4" />
                          {fmt.toUpperCase()}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <AnimatePresence>
          {message && (
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 50 }}
              className={`fixed bottom-8 left-1/2 -translate-x-1/2 px-6 py-3 rounded-full shadow-2xl flex items-center gap-3 ${
                message.type === 'error' ? 'bg-red-500 text-white' : 'bg-green-500 text-white'
              }`}
            >
              {message.type === 'success' ? <CheckCircle className="w-5 h-5" /> : <div className="w-5 h-5 font-bold">!</div>}
              {message.text}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
