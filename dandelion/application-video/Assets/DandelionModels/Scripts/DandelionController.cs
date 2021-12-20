using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DandelionController : MonoBehaviour
{
    public GameObject topSeeds;
    public ParticleSystem ps;
    // Start is called before the first frame update
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        if( Input.GetKeyDown(KeyCode.B) )
        {
            Blow();
        }
    }

    public void Blow()
    {
        StartCoroutine(RemoveTop());
        ps.Play();
    }

    IEnumerator RemoveTop()
    {
        yield return new WaitForSeconds(0.2f);
        topSeeds.SetActive(false);
    }
}
