using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DandelionWalker : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        GetComponent<Rigidbody>().velocity = Vector3.back * 1.1f;
    }

    // Update is called once per frame
    void Update()
    {

    }

    void OnTriggerEnter(Collider c)
    {
        GetComponent<DandelionController>().Blow();
    }

    void OnTriggerExit(Collider c)
    {
        gameObject.SetActive(false);
    }
}
