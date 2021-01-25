using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class UProfilerDemo : MonoBehaviour
{
    // Start is called before the first frame update
    public void OnStart()
    {
        UProfiler.Instance().StartProfiler();
    }

    public void OnStop()
    {
        UProfiler.Instance().StopProfiler();
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
