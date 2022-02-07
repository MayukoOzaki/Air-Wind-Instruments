using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.IO;
using System.Text;

public class NoteLayout : MonoBehaviour
{

    [SerializeField] public TextAsset toneFile;
    List<string[]> toneDatas = new List<string[]>();

    // Start is called before the first frame update
    void Start()
    {
        ReadText(toneFile);

        Debug.Log(toneDatas.Count);         // s”
        Debug.Log(toneDatas[0].Length);       // €–Ú”
        Debug.Log(toneDatas[1][2]);        // 2s–Ú3—ñ–Ú

    }

    void ReadText(TextAsset fileName)
    {
        string[] lines = fileName.text.Replace("\r\n", "\n").Split("\n"[0]);
        foreach (var line in lines)
        {
            if (line == "") { continue; }
            toneDatas.Add(line.Split(' '));    // string[]‚ğ’Ç‰Á‚µ‚Ä‚¢‚é
        }

    }

    // Update is called once per frame
    void Update()
    {
        
    }

}
