using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GCDemo : MonoBehaviour
{
    List<int[]> m_Contianer = new List<int[]>();
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        m_Contianer.Add(new int[1024]);
    }
}
