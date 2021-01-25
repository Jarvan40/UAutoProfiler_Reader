using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.Profiling;

public class UProfiler
{
    private static UProfiler m_Instance;
    public static UProfiler Instance()
    {
        if(m_Instance == null)
        {
            m_Instance = new UProfiler();
        }
        return m_Instance;
    }

    private string m_DataPath = Application.persistentDataPath + "/uBox";
    
    public bool StartProfiler()
    {
        if (Profiler.supported)
        {
            if (Profiler.enableBinaryLog)
            {
                Debug.Log("[UBox]-Error Game Is Profilering");
                return false;
            }

            if (!Directory.Exists(m_DataPath))
            {
                Directory.CreateDirectory(m_DataPath);
            }

            //某些版本存在bug，因此设置此参数 让其自动扩展
#if !UNITY_5_4_OR_NEWER && UNITY_5_1_OR_NEWER
            Profiler.maxNumberOfSamplesPerFrame = -1;
#endif

#if UNITY_2017_4_OR_NEWER
            Profiler.logFile = m_DataPath + "/P.data";
#else
            Profiler.logFile = "P1.txt";
#endif
            Profiler.enableBinaryLog = true;                        
            //如果unity版本高于或等于2018.3，需手动开启要收集的数据区域
#if UNITY_2018_3_OR_NEWER
            Profiler.SetAreaEnabled(ProfilerArea.CPU, true);
            Profiler.SetAreaEnabled(ProfilerArea.Rendering, true);
            Profiler.SetAreaEnabled(ProfilerArea.GPU, true);
            Profiler.SetAreaEnabled(ProfilerArea.Memory, true);
            Profiler.SetAreaEnabled(ProfilerArea.Physics, true);
            //Profiler.SetAreaEnabled(ProfilerArea.GlobalIllumination, true);
            Profiler.maxUsedMemory = 512 * 1024 * 1024;
#endif
            Profiler.enabled = true;
            Debug.LogFormat("[Ubox]-Info Log Profile To {0}", m_DataPath);
            return true;
        }
        else
        {
            Debug.LogError("[UBox]-Error Enabling profiling is not supported.");
            return false;
        }        
    }

    public bool StopProfiler()
    {
        if(Profiler.enableBinaryLog)
        {
            Profiler.enableBinaryLog = false;
            Profiler.enabled = false;
        }
        Debug.LogFormat("[UBox]-Info StopProfiler {0}", m_DataPath);
        return Profiler.enableBinaryLog;
    }

    #region Version
    public string GetVersion()
    {
        return "1.0";
    }
    #endregion
}
