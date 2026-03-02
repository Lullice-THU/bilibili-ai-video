import { useState } from 'react'
import { View, Text, Textarea, Button, Loading } from '@tarojs/components'
import './index.css'

const API_BASE = 'http://localhost:8000'

export default function Index() {
  const [material, setMaterial] = useState('')
  const [title, setTitle] = useState('')
  const [script, setScript] = useState('')
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)
  const [error, setError] = useState('')

  const handleGenerate = async () => {
    if (!material || material.trim().length < 10) {
      return
    }

    setLoading(true)
    setTitle('')
    setScript('')

    try {
      const res = await fetch(`${API_BASE}/api/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          material: material,
          video_type: 'general'
        })
      })
      const data = await res.json()
      
      if (data.success) {
        setTitle(data.title)
        setScript(data.script)
        setError('')
      } else {
        setError(data.error || '生成失败，请重试')
        console.error('生成失败:', data.error)
      }
    } catch (err) {
      setError('请求失败，请检查网络或后端服务')
      console.error('请求失败:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    const text = `标题：${title}\n\n文案：\n${script}`
    // H5 环境使用 Clipboard API
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => {
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      })
    } else {
      // 兼容方案
      const textarea = document.createElement('textarea')
      textarea.value = text
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <View className='container'>
      <View className='header'>
        <Text className='title'>🎬 Bilibili AI 助手</Text>
        <Text className='subtitle'>输入素材 → AI 生成文案 → 一键复制</Text>
      </View>

      <View className='input-section'>
        <Text className='label'>📝 输入素材内容</Text>
        <Textarea
          className='material-input'
          placeholder='粘贴你的视频素材、文案、链接...'
          value={material}
          onInput={(e) => setMaterial(e.detail.value)}
          maxlength={5000}
        />
        <Text className='char-count'>{material.length}/5000</Text>
      </View>

      <Button
        className={`generate-btn ${loading ? 'loading' : ''}`}
        onClick={handleGenerate}
        disabled={loading || material.trim().length < 10}
      >
        {loading ? <Loading color='#fff' /> : '🚀 AI 生成文案'}
      </Button>

      {error && (
        <View className='error-tip'>
          <Text>{error}</Text>
        </View>
      )}

      {(title || script) && (
        <View className='result-section'>
          <Text className='label'>📌 生成标题</Text>
          <View className='result-box title-box'>
            <Text>{title}</Text>
          </View>

          <Text className='label'>📄 生成文案</Text>
          <View className='result-box script-box'>
            <Text className='script-text'>{script}</Text>
          </View>

          <Button className='copy-btn' onClick={handleCopy}>
            {copied ? '✅ 已复制!' : '📋 一键复制全部'}
          </Button>
        </View>
      )}
    </View>
  )
}
