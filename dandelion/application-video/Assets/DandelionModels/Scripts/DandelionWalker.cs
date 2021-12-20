using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DandelionWalker : MonoBehaviour
{
    public GameObject camera;
    bool isBlown;
    // Start is called before the first frame update
    void Start()
    {
        isBlown = false;
        camera = GameObject.FindGameObjectWithTag("MainCamera");
    }

    // Update is called once per frame
    void Update()
    {

    }

    void OnTriggerEnter(Collider c)
    {
        if( !isBlown )
        {
            isBlown = true;
            Vector3 dir = transform.position - camera.gameObject.transform.position;
            Debug.Log(dir);
            GetComponent<DandelionController>().Blow(dir);
            Debug.Log("here");
        }
    }

    void OnTriggerExit(Collider c)
    {
        gameObject.SetActive(false);
    }
}